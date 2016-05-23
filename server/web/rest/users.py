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
from server.web.utils import has_permission, get_token_from_request, jsonify

users_v1_blueprint = Blueprint('users_v1_api', __name__)


def setup_user_from_request():
    """
    Get the user from the request headers and store on the g
    object for later use.
    """
    try:
        token = get_token_from_request()
        if token is not None:
            g.user = user_service.get_user_from_token(token)
    except (TokenException, ResourceDoesNotExistException):
        g.user = None


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
    role = data.get('role')

    if role is None:
        raise ValidationException('You must define a role to create a new user.')
    elif role != 'supplychainmanager' and \
            role != 'retailstoremanager' and \
            g.user is not None and \
            not user_service.has_permission(g.user, 'edit_users'):
        raise AuthorizationException('You don\'t have permission to set roles.')

    user = user_service.create_user(user_id=data.get('id'),
                                    email=data.get('email'),
                                    role=role,
                                    password=data.get('password'))

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
    user = user_service.get_user_by_id(user_id)
    if not user_service.is_owner(g.user, user):
        user_service.check_permission(g.user, 'view_users')
    return Response(jsonify(user, user_service.user_to_dict))


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
    data = request.get_json()

    user = user_service.get_user_by_id(user_id)
    if not user_service.is_owner(g.user, user):
        user_service.check_permission(g.user, 'edit_users')

    # We have now confirmed a user is updating their own profile
    user_dict = user_service.teacher_to_dict(user)

    # Make sure PUT requests received complete user object
    if request.method == 'PUT':
        for key in user_dict:
            if key not in data:
                raise ValidationException(
                    'Must pass full user representation.')

    user_service.update_teacher(user, data)
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
        "id": "eyJhbGciOi...WT2aGgjY5JHvCsbA",
        "ttl": "1440",
        "createdAt": "2015-11-05T22:00:51.692765",
        "userId": "test@example.com"
    }
    """
    data = request.get_json()
    token = user_service.authenticate(user_id=data.get('user_id'),
                                     password=data.get('password'))
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
    if request_token == token or \
            user_service.check_permission(g.user, 'delete_sessions'):
        try:
            # TODO: Invalidate JWT so session expires
            pass
        except ResourceDoesNotExistException:
            pass
    return '', 204


@users_v1_blueprint.route('/users', methods=['GET'])
@has_permission('view_users')
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
    users = user_service.list_users()
    return Response(jsonify(users, user_service.user_to_dict))
