"""
A module containing utilities that are helpful within the Flask context.
Anything that may apply for all interfaces. This may depend on the current
Flask app and request.
"""
import json

from decorator import decorator
from flask import g, request

from server.exceptions import (AuthorizationException,
                               TokenException)
import server.services.users as user_service


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


def has_permission(*permissions):
    """
    Decorator for checking that the user is authenticated and
    has proper permissions to access resource.

    :param permissions:
    :return:
    """

    @decorator
    def decorator_function(func, *args, **kwargs):
        if g.user is None:
            raise AuthorizationException('Unable to identify user')
        elif not user_service.has_permission(g.user, *permissions):
            raise AuthorizationException('Insufficient permissions.')

        return func(*args, **kwargs)

    return decorator_function


@decorator
def logged_in(func, *args, **kwargs):
    if g.user is None:
        raise AuthorizationException('No user logged in.')
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
    Convert an instance or a list of instances of the User model
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