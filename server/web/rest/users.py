"""
The REST interface for user resources. This interface also handles
authentication resources.
"""
import json

import server.services.users as user_service
from flask import g, request, Response, url_for, Blueprint
from server.exceptions import (TokenException,
                               AuthorizationException,
                               ResourceDoesNotExistException,
                               ValidationException)
from server.web.utils import get_token_from_request, jsonify

users_v1_blueprint = Blueprint('users_v1_api', __name__)


def setup_auth_from_request():
    """
    Get the Auth data from the request headers and store on the g
    object for later use.
    """
    try:
        token = get_token_from_request()
        if token is not None:
            g.auth = user_service.get_auth_from_token(token)
    except (TokenException, ResourceDoesNotExistException):
        g.auth = None


@users_v1_blueprint.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user resource. This does not require any special permissions.

    :param: {
        "id": "test@example.com",
        "email": "test@example.com",
        "password": "password",
        "role": "supplychainmanager"
    }

    :return: {
        "id": "test@example.com",
        "email": "test@example.com",
        "role": "supplychainmanager"
        "createdAt": "2015-11-05T22:00:51.692765"
    }

    """
    data = request.get_json()
    user_id = data.get('id')
    email = data.get('email')
    role = data.get('role')
    password = data.get('password')

    if user_id is None:
        raise ValidationException('You must define a username to create a new user.')
    elif email is None:
        raise ValidationException('You must include an email to create a new user.')
    elif role is None:
        raise ValidationException('You must define a role to create a new user.')
    elif password is None:
        raise ValidationException('You must set a password to create a new user.')

    user = user_service.create_user(auth=g.auth,
                                    user_id=user_id,
                                    email=email,
                                    role=role,
                                    password=password)

    return Response(jsonify(user, user_service.user_to_dict),
                    status=201,
                    mimetype='application/json')


@users_v1_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a single user object.

    :param user_id:   The user's id.

    :return: {
        "id": "test@example.com",
        "email": "test@example.com",
        "role": "supplychainmanager",
        "created": "2015-11-05T22:00:51.692765"
    }
    """
    user = user_service.get_user_by_id(g.auth, user_id)
    return Response(jsonify(user, user_service.user_to_dict),
                    status=200,
                    mimetype='application/json')


@users_v1_blueprint.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    """
    Update a user.

    When using PUT, you must pass an entire representation of a user. To
    Update only specific fields, use PATCH.

    :param:   {
        "id": "test@example.com",
        "email": "test@example.com",
        "role": "supplychainmanager",
        "created": "2015-11-05T22:00:51.692765"
    }

    :return: {
        "id": "test@example.com",
        "email": "test@example.com",
        "role": "supplychainmanager",
        "created": "2015-11-05T22:00:51.692765"
    }
    """
    if user_id is None:
        raise ValidationException('You must include a user_id to designate the user to be updated')

    data = request.get_json()
    user = user_service.update_user(g.auth, user_id, data)
    return Response(jsonify(user, user_service.user_to_dict))


@users_v1_blueprint.route('/auth', methods=['POST'])
def authenticate():
    """
    Authenticate a user and get an authorization token. This token should
    then be passed via the Authorization header:

    'Authorization: Bearer eyJhbGciOi...WT2aGgjY5JHvCsbA'

    :param: {
        "id": "test@example.com",
        "password": "password"
    }

    :return: {
        "token": "eyJhbGciOi...WT2aGgjY5JHvCsbA"
    }
    """
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    if user_id is None:
        raise ValidationException('You must a username when logging in.')
    elif password is None:
        raise ValidationException('You must include a password when logging in.')
    auth_data = user_service.login(user_id=user_id,
                                   password=password)

    # TODO: Determine the desired session length (currently defaulted to 1 day)
    token = user_service.get_token_for_user(auth_data, expire_days=1)

    resp = Response(json.dumps({'token': token}),
                    status=200,
                    mimetype='application/json')
    resp.set_cookie('auth_token', token, httponly=True)
    return resp


@users_v1_blueprint.route('/auth/<string:token>', methods=['DELETE'])
def deauthenticate(token):
    """
    Logout the current user
    :param token  Current web token
    :return:
    """
    request_token = get_token_from_request()

    # Only allow deletion of a web token if the token belongs to the current user,
    # or if the current user has the delete permission (currently only admins)
    if request_token == token:
        user_service.logout(token=g.auth['loopback_token'])
    return '', 204


@users_v1_blueprint.route('/users', methods=['GET'])
def list_users():
    """
    List all users. Requires administrator privileges.

    :return: [{
        "id": "test@example.com",
        "email": "test@example.com",
        "role": "supplychainmanager",
        "createdAt": "2015-11-05T22:00:51.692765"
    }, {...}]
    """
    users = user_service.list_users(g.auth)
    return Response(jsonify(users, user_service.user_to_dict))
