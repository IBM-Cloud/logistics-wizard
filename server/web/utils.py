"""
A module containing utilities that are helpful within the Flask context.
Anything that may apply for all interfaces. This may depend on the current
Flask app and request.
"""
import jwt
from server.config import Config
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
        token = header.split()[1] if header is not None else request.cookies.get('auth_token')
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


def check_null_input(*fields):
    """
    Checks a list of params and raises a ValidationException if None

    :param fields:  List of (param, error) tuples to check for null values
    """
    for field in fields:
        if field[0] is None:
            raise ValidationException('You must specify a %s' % field[1])


def compose_error(exc, e):
    """
    Composes an error to return to the client after APIException is thrown

    :param exc:     Raised exception
    :param e:       Returned error
    :return:        An string to specify the error if param is None
    """
    return_error = dict(code=exc.status_code,
                        message=e.message)

    if hasattr(e, 'user_details') and e.user_details is not None:
        return_error['user_details'] = e.user_details

    return return_error


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
        raise TokenException('Error decoding JWT token.', internal_details=str(e))

    return data
