"""
Handle all interactions with the Service Discovery service.
"""
import json
import time
import requests
from threading import Thread
from server.config import Config
from server.exceptions import (APIException, ValidationException,
                               AuthenticationException, ResourceDoesNotExistException)

###########################
#         Utilities       #
###########################


def heartbeater(service_id, heartbeat):
    while True:
        time.sleep(heartbeat)
        heartbeat_service(service_id)


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
#         Services        #
###########################


def get_services(fields=None, tags=None, service_name=None, status=None):
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

    retrieve_services_url = '%s/api/v1/instances?%s' % (Config.SD_URL,status_query)
    headers = {'Authorization': 'Bearer %s' % Config.SD_AUTH}

    try:
        response = requests.request("GET", retrieve_services_url, headers=headers)
    except Exception as e:
        raise APIException('Error on service lookup', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 400:
        raise ValidationException('Bad request to service registry',
                                  internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 401:
        raise AuthenticationException('Unauthorized service lookup: token is not valid',
                                      internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 404:
        raise AuthenticationException('Service Discovery endpoint not found',
                                      internal_details=json.loads(response.text).get('Error'))

    return response.text


def register_service(service_name, ttl, status, endpoint, protocol, heartbeat=True, tags=None):
    """
    Registers the service according to the input configs.

    :param service_name:    Name of the service.
    :param ttl:             Time (sec) in which the service must register a heartbeat.
    :param status:          Starting status of the service.
    :param endpoint:        Endpoint of the service.
    :param protocol:        Desired protocol of the service endpoint.
    :param heartbeat:       Indicates whether or not to spawn a heartbeat thread.
    :param tags:            (Optional) Tags to associate with the service.

    :return response
    """

    register_url = '%s/api/v1/instances' % Config.SD_URL
    sd_registration_payload = {
        'tags': tags,
        'status': status,
        'service_name': service_name,
        'ttl': ttl,
        'endpoint': {
            'value': endpoint,
            'type': protocol
        }
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer %s' % Config.SD_AUTH
    }

    try:
        response = requests.request("POST", register_url, data=json.dumps(sd_registration_payload), headers=headers)
    except Exception as e:
        raise APIException('Error registering controller service', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 400:
        raise ValidationException('Bad request to service registry',
                                  internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 401:
        raise AuthenticationException('Unauthorized service registration: token is not valid',
                                      internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 404:
        raise AuthenticationException('Service Discovery endpoint not found',
                                      internal_details=json.loads(response.text).get('Error'))

    # Spawn thread responsible for sending heartbeat
    if heartbeat:
        t = Thread(target=heartbeater,
                   kwargs={'service_id': json.loads(response.text).get('id'), 'heartbeat': round(ttl*.75)})
        t.start()

    return response.text


def heartbeat_service(service_id):
    """
    Heartbeat the service with the input id.

    :param service_id:  The ID of the service to heartbeat.

    :return response
    """

    heartbeat_url = '%s/api/v1/instances/%s/heartbeat' % (Config.SD_URL, service_id)
    headers = {'Authorization': 'Bearer %s' % Config.SD_AUTH}

    try:
        response = requests.request("PUT", heartbeat_url, headers=headers)
    except Exception as e:
        raise APIException('Error heartbeating service', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 400:
        raise ValidationException('Bad request to service registry',
                                  internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 401:
        raise AuthenticationException('Unauthorized service heartbeat: token is not valid',
                                      internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Service Discovery endpoint not found',
                                            internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 410:
        raise ResourceDoesNotExistException('Service instance not found',
                                            internal_details=json.loads(response.text).get('Error'))


def deregister_service(service_id):
    """
    De-register the service with the input id.

    :param service_id:  The ID of the service to de-register.

    :return response
    """

    heartbeat_url = '%s/api/v1/instances/%s' % (Config.SD_URL, service_id)
    headers = {'Authorization': 'Bearer %s' % Config.SD_AUTH}

    try:
        response = requests.request("DELETE", heartbeat_url, headers=headers)
    except Exception as e:
        raise APIException('Error de-registering service', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 400:
        raise ValidationException('Bad request to service registry',
                                  internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 401:
        raise AuthenticationException('Unauthorized service de-registration: token is not valid',
                                      internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Service Discovery endpoint not found',
                                            internal_details=json.loads(response.text).get('Error'))
    elif response.status_code == 410:
        raise ResourceDoesNotExistException('Service instance not found',
                                            internal_details=json.loads(response.text).get('Error'))
