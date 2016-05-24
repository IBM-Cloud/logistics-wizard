"""
A module containing utilities that are helpful within the Flask context.
Anything that may apply for all interfaces. This may depend on the current
Flask app and request.
"""
import json

from flask import g, request

from server.exceptions import (TokenException)

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
