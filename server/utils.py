"""
High level utilities, can be used by any of the layers (data, service,
interface) and should not have any dependency on Flask or request context.
"""
import re
from types import FunctionType
from os import environ as env
from json import loads
from server.config import Config
from server.exceptions import APIException
from bluemix_service_discovery.service_locator import ServiceLocator


def validate_email(email_address):
    """
    Verify that the email is a valid email address
    """
    email_regex = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+"
                             "(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
                             "@"
                             "(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
                             "[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

    if email_regex.match(email_address) is None:
        return False
    else:
        return True


def async_helper(args):
    """
    Calls the passed in function with the input arguments. Used to mitigate
    calling different functions during multiprocessing

    :param args:    Function and its arguments
    :return:        Result of the called function
    """

    # Isolate function arguments in their own tuple and then call the function
    func_args = tuple(y for y in args if type(y) != FunctionType)
    return args[0](*func_args)


def get_service_url(service_name):
    """
    Retrieves the URL of the service being called based on the environment
    that the controller is currently being run.

    :param service_name:    Name of the service being retrieved
    :return:                The endpoint of the input service name
    """

    # Use the Service Discovery service if Prod and toggle is on
    if Config.ENVIRONMENT == 'PROD' and Config.SD_STATUS == 'ON' and env.get('VCAP_SERVICES') is not None:
        try:
            creds = loads(env['VCAP_SERVICES'])['service_discovery'][0]['credentials']
            locator = ServiceLocator(creds['url'], creds['auth_token'])
            service_instances = loads(locator.get_services(service_name=service_name, status='UP'))['instances']
            if len(service_instances) == 0:
                raise APIException('Dependent service not available')
            return 'https://%s' % service_instances[0]['endpoint']['value']
        except Exception as e:
            if isinstance(e, Exception):
                e = e.message
            raise APIException('Cannot get dependent service', user_details=str(e), internal_details=str(e))
    # Otherwise, get the service endpoint from an env var
    else:
        if service_name == 'lw-erp':
            return env['ERP_SERVICE']
        elif service_name == 'lw-recommendation':
            return env['RECOMMENDATION_SERVICE']
        else:
            raise APIException('Unrecognized service invocation')
