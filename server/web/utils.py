"""
A module containing utilities that are helpful within the Flask context.
Anything that may apply for all interfaces. This may depend on the current
Flask app and request.
"""
import json

from decorator import decorator
from flask import g, request

from server.exceptions import (AuthorizationException,
                               TokenException,
                               ValidationException)

###########################
#     Request Utils       #
###########################


def get_token_from_request():
    """
    Pulls the auth token from the request headers.

    :return:  Auth token if it exists, else None.
    """
    token = None
    try:
        header = request.headers.get('Authorization')
        if header is not None:
            token = header.split()[1]
        else:
            token = request.cookies.get('auth_token')
    except (AttributeError, IndexError):
        pass

    if token is None:
        raise TokenException('Unable to get token from request.')

    return token


@decorator
def logged_in(func, *args, **kwargs):
    if g.auth is None:
        raise AuthorizationException('No existing session.')
    else:
        return func(*args, **kwargs)


def _default_mapper(x):
    """
    The default mapper expects a dict and returns it.
    :param x:    A dict.
    :return: x
    """
    return x


def jsonify(resource, dict_mapper, **kwargs):
    """
    Convert an instance or a list of instances of the resource model
    to JSON.

    :param resource:     An instance or a list of instances of the resource
                         model.
    :param dict_mapper:  A function to convert the resource to a dict.
    :return:             A JSON string.
    """
    if dict_mapper is not None:
        mapper = dict_mapper
    else:
        mapper = _default_mapper

    if isinstance(resource, list):
        json_string = json.dumps([mapper(x, **kwargs) for x in resource])
    else:
        json_string = json.dumps(mapper(resource, **kwargs))
    return json_string


def request_wants_json():
    best = request.accept_mimetypes.best_match(['text/html', 'application/json'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


def get_json_data(req):
    """
    Takes a request and extracts the JSON from the body

    :param req:     An API request
    :return:        A JSON object.
    """
    try:
        return req.get_json()
    except Exception:
        raise ValidationException('No JSON payload received in the request')


def check_null_input(param, error_string):
    """
    Checks a param and raises a ValidationException if None

    :param param:           An API input parameter
    :param error_string:    An string to specify the error if param is None
    """
    if param is None:
        raise ValidationException('You must specify {0} '.format(error_string))


def compose_error(exc, e):
    """
    Composes an error to return to the client after APIException is thrown

    :param exc:     Raised exception
    :param e:       Returned error
    :return:        An string to specify the error if param is None
    """
    return_error = dict(code=exc.status_code,
                        message=e.message)
    if e.user_details is not None:
        return_error['user_details'] = e.user_details

    return return_error

