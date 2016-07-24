"""
Wrapper for the Bluemix Service Discovery service.
"""
import json
import time
import requests
from threading import Thread
from os import environ as env

###########################
#         Utilities       #
###########################


def load_credentials(url=None, auth_token=None):
    """
    Returns the Service Discovery credentials, if available

    :param url:         Service Discovery API URL
    :param auth_token:  Access token for Service Discovery
    :return:            The URL and Auth credentials
    """
    if env.get('VCAP_SERVICES') is not None:
        return {
            'url': json.loads(env['VCAP_SERVICES'])['service_discovery'][0]['credentials']['url'],
            'auth_token': json.loads(env['VCAP_SERVICES'])['service_discovery'][0]['credentials']['auth_token']
        }
    else:
        if auth_token is None:
            raise Exception("An auth token is required for Service Discovery")
        return {
            'url': url if url is not None else "https://servicediscovery.ng.bluemix.net",
            'auth_token': auth_token
        }


def add_query_filter(cur_query, param, value):
    """
    Add a query condition to an input query string

    :param cur_query:   Current query string.
    :param param:       Filter to apply.
    :param value:       Value to filter on.

    :return:            The updated query string.
    """

    # If the query string is null, initialize it
    # If it is non-empty, separate from new query with ampersand
    if cur_query is None:
        cur_query = ""
    elif cur_query != "":
        cur_query += "&"

    return '%s%s=%s' % (cur_query, param, value)

###########################
#         Classes         #
###########################


class ServicePublisher:
    """Register and heartbeat a new service instance"""

    def __init__(self, name, ttl, status, endpoint, protocol, tags=None, url=None, auth_token=None):
        """
        Initializes the service instance with all its parameters.

        :param name:        Name of the service.
        :param ttl:         Time (sec) in which the service must register a heartbeat.
        :param status:      Starting status of the service.
        :param endpoint:    Endpoint of the service.
        :param protocol:    Desired protocol of the service endpoint.
        :param tags:        Tags to associate with the service.
        :param url:         Service Discovery API endpoint.
        :param auth_token:  Authorization token for Service Discovery.
        """
        self.name = name
        self.ttl = ttl
        self.status = status
        self.endpoint = {
            'value': endpoint,
            'type': protocol
        }
        self.tags = [] if tags is None else tags

        # Get credentials
        credentials = load_credentials(url, auth_token)
        self.url = credentials['url']
        self.token = credentials['auth_token']

        # Uninitialized vars
        self.heartbeats = []
        self.heartbeat_thread = None
        self.id = None

        # Flags
        self.beating = False
        self.registered = False

    def register_service(self, heartbeat=True):
        """
        Registers the service with Service Discovery.

        :param heartbeat:   Indicates whether or not to spawn a heartbeat thread.
        :return:            Successful service registration object
        """

        # Create the API request payload and headers
        registration_payload = {
            'tags': self.tags,
            'status': self.status,
            'service_name': self.name,
            'ttl': self.ttl,
            'endpoint': self.endpoint
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer %s' % self.token
        }

        # Call Service Discovery /instances to register the service
        try:
            response = requests.request("POST",
                                        '%s/api/v1/instances' % self.url,
                                        data=json.dumps(registration_payload),
                                        headers=headers)
        except Exception as e:
            raise Exception('Error registering controller service', str(e))

        # Check for possible errors in response
        if response.status_code == 400:
            raise Exception('Bad request to service registry',
                            json.loads(response.text).get('Error'))
        elif response.status_code == 401:
            raise Exception('Unauthorized service registration: token is not valid',
                            json.loads(response.text).get('Error'))

        # Spawn thread responsible for sending heartbeat
        self.registered = True
        self.id = json.loads(response.text).get('id')
        if heartbeat:
            self.heartbeat_thread = Thread(target=self._heartbeater,
                                           kwargs={'interval': round(self.ttl*.5)})
            self.heartbeat_thread.start()

        return response.text

    def heartbeat_service(self):
        """
        Heartbeats the service with Service Discovery.
        """

        # First make sure service has been registered
        if not self.registered:
            raise Exception('Service instance is not registered')

        # Call Service Discovery /instances/XXX/heartbeat to heartbeat the service
        try:
            response = requests.request("PUT",
                                        '%s/api/v1/instances/%s/heartbeat' % (self.url, self.id),
                                        headers={'Authorization': 'Bearer %s' % self.token})
        except Exception as e:
            raise Exception('Error heartbeating service', str(e))

        # Check for possible errors in response
        if response.status_code == 400:
            raise Exception('Bad request to service registry',
                            json.loads(response.text).get('Error'))
        elif response.status_code == 401:
            raise Exception('Unauthorized service heartbeat: token is not valid',
                            json.loads(response.text).get('Error'))
        elif response.status_code == 410:
            raise Exception('Service instance not found',
                            json.loads(response.text).get('Error'))

        # Add heartbeat to list
        heartbeat_time = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
        self.heartbeats.append(heartbeat_time)
        return heartbeat_time

    def _heartbeater(self, interval):
        """
        Handles the service heartbeat

        :param: interval    Time lapse (sec) between heartbeats
        """
        self.beating = True
        while self.beating:
            time.sleep(interval)
            self.heartbeat_service()

    def get_last_heartbeat(self):
        """
        Returns the datetime of the last heartbeat

        :return:    Datetime string of the last service heartbeat
        """
        if len(self.heartbeats) > 0:
            return self.heartbeats[-1]
        else:
            return ''

    def deregister_service(self):
        """
        De-register the service with Service Discovery
        """

        # Stop the heartbeats
        if self.beating:
            self.beating = False
            self.heartbeat_thread.join()
            self.heartbeats = []

        # Call Service Discovery /instances/XXX to re-register the service
        try:
            response = requests.request("DELETE",
                                        '%s/api/v1/instances/%s' % (self.url, self.id),
                                        headers={'Authorization': 'Bearer %s' % self.token})
        except Exception as e:
            raise Exception('Error de-registering service', str(e))

        # Check for possible errors in response
        if response.status_code == 400:
            raise Exception('Bad request to service registry',
                            json.loads(response.text).get('Error'))
        elif response.status_code == 401:
            raise Exception('Unauthorized service de-registration: token is not valid',
                            json.loads(response.text).get('Error'))
        elif response.status_code == 410:
            raise Exception('Service instance not found',
                            json.loads(response.text).get('Error'))

        self.registered = False


class ServiceLocator:
    """Search for service instances"""

    def __init__(self, url=None, auth_token=None):
        """
        Initializes the service instance with all its parameters.

        :param url:         Service Discovery API endpoint.
        :param auth_token:  Authorization token for Service Discovery.
        """

        # Get credentials
        credentials = load_credentials(url, auth_token)
        self.url = credentials['url']
        self.token = credentials['auth_token']

    def get_services(self, fields=None, tags=None, service_name=None, status=None):
        """
        Returns all the currently registered services and their parameters.

        :param fields       Comma separated list of fields to include in response.
        :param tags         Comma separated list of tags that returned instances must have.
        :param service_name Name of instances to return.
        :param status       State of instances to be return.

        :return response
        """

        # Add filters if corresponding inputs are present
        status_query = ""
        if fields is not None:
            status_query = add_query_filter(status_query, "fields", fields)
        if tags is not None:
            status_query = add_query_filter(status_query, "tags", tags)
        if service_name is not None:
            status_query = add_query_filter(status_query, "service_name", service_name)
        if status is not None:
            status_query = add_query_filter(status_query, "status", status)

        retrieve_services_url = '%s/api/v1/instances?%s' % (self.url, status_query)
        headers = {'Authorization': 'Bearer %s' % self.token}

        try:
            response = requests.request("GET", retrieve_services_url, headers=headers)
        except Exception as e:
            raise Exception('Error on service lookup', str(e))

        # Check for possible errors in response
        if response.status_code == 400:
            raise Exception('Bad request to service registry',
                            json.loads(response.text).get('Error'))
        elif response.status_code == 401:
            raise Exception('Unauthorized service lookup: token is not valid',
                            json.loads(response.text).get('Error'))

        return response.text
