"""
High level utilities, can be used by any of the layers (data, service,
interface) and should not have any dependency on Flask or request context.
"""
import jwt
import re
from types import FunctionType
from os import environ as env
from json import loads
from server.config import Config
from server.exceptions import APIException, TokenException
from server.service_discovery import ServiceLocator


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


def tokenize(data):
    """
    Creates a signed JSON Web Token of the data.

    :param data:  Any dict to be tokenized.
    :return:      A signed token representing the data.
    """
    return jwt.encode(data, Config.SECRET)


def detokenize(token):
    """
    Convert a token to a dict. Raises a TokenException if the token is
    expired or tampered with.

    :param token:   The token to be converted.
    :return:
    """
    try:
        data = jwt.decode(token, Config.SECRET)
    except Exception as e:
        raise TokenException('Error decoding JWT token.',
                             internal_details=str(e))

    return data

# Map of extensions to content types
_EXT_MAP = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'pdf': 'application/pdf'
}


def get_content_type_from_ext(ext):
    """
    Get the content type associated with this files extension.
    :param ext:    A file extension.
    :return:       A MIME content type.
    """
    return _EXT_MAP.get(ext.replace('.', ''), None)


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
            locator = ServiceLocator(loads(env['VCAP_SERVICES'])['service_discovery'][0]['credentials']['url'],
                                     loads(env['VCAP_SERVICES'])['service_discovery'][0]['credentials']['auth_token'])
            service_instances = loads(locator.get_services(service_name=service_name, status='UP'))['instances']
            if len(service_instances) == 0:
                raise APIException('Dependent service not available')
            return service_instances[0]['endpoint']['value']
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
