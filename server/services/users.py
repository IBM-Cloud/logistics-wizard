"""
Handle all actions on the user resource and is responsible for making sure
the data gets into the database. As much as possible, the interface layer should
have no knowledge of the properties of the user object and should just call
into the service layer to act upon a user resource.
"""
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from server.exceptions import (TokenException,
                               IntegrityException,
                               ResourceDoesNotExistException,
                               AuthenticationException,
                               AuthorizationException)
from server.utils import tokenize, detokenize


###########################
#         Utilities       #
###########################


def user_to_dict(user):
    """
    Convert an instance of the User model to a dict.

    :param user:  An instance of the User model.
    :return:      A dict representing the user.
    """

    return {
        'user_id': user.user_id,
        'email': user.email,
        'role': user.role,
        'createdAt': user.created.isoformat()
    }


###########################
#         Services        #
###########################


def create_user(auth=None, user_id=None, email=None, role=None, password=None):
    """
    Create a new user in the ERP system.

    :param auth:     Auth info for the request.
    :param user_id:  The user's id. Optional, defaults to email.
    :param email:    The user's email address.
    :param password: The user's cleartext password (will be hashed).
    :param role:     The user's role.
    :return:         The created User model.
    """
    if user_id is None:
        user_id = email
    try:
        # TODO: Call ERP API to create a user
        user = {
            'id': "test@example.com",
            'email': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        }
    except IntegrityError as e:
        raise IntegrityException('User already exists', internal_details=str(e))
    return user


def update_user(auth, user_id, user):
    """
    Create a new user in the ERP system.

    :param auth:    Auth info for the request.
    :param user_id:    The user's id
    :param user:    The user's id
    :return:        The updated User model.
    """
    try:
        # TODO: Call ERP API to update the user
        user = {
            'id': "test@example.com",
            'email': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('User does not exist', internal_details=str(e))
    return user


def list_users(auth):
    """
    List all users in the ERP system

    :param auth:    Auth info for the request.
    :return:        An array of instances of Users.
    """
    try:
        # TODO: Call ERP API to get users
        users = list()
        users.append({
            'id': "test@example.com",
            'email': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        })
    except IntegrityError as e:
        pass
    return users


def get_user_by_id(auth, user_id):
    """
    Retrieve a user from the ERP system by psk.

    :param auth:      Auth info for the request.
    :param user_id:   The user's id.
    :return:          An instance of the User.
    """
    try:
        # TODO: Call ERP API to get the user
        user = {
            'id': "test@example.com",
            'email': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('User does not exist', internal_details=str(e))
    return user


def get_user_by_email(auth, email):
    """
    Retrieve a user from the ERP system by email.

    :param auth:    Auth info for the request.
    :param email:   The user's email.
    :return:        An instance of the User.
    """
    try:
        # TODO: Call ERP API to get the user
        user = {
            'id': "test@example.com",
            'email': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('User does not exist', internal_details=str(e))
    return user


def get_user_role(auth, user_id):
    """
    Get the role for this user.

    :param auth:       Auth info for the request.
    :param user_id:    The user_id for which to get the role.
    :return:           The role for this user
    """
    try:
        # TODO: Call ERP API to get the user's role
        user = {
            'id': "test@example.com",
            'email': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('User does not exist', internal_details=str(e))
    return user


def login(user_id=None, password=None):
    """
    Authenticate a user against the ERP system.

    :param user_id:     The user_id for which to log in.
    :param password:    The user's password.
    :return:            Auth data returned by ERP system
    """
    try:
        # TODO: Call ERP API to log the user in
        auth_data = {
            'loopback_token': "123",
            'id': "test@example.com",
            'role': "supplychainmanager"
        }
    except ResourceDoesNotExistException:
        raise AuthenticationException('User does not exist')

    return auth_data


def logout(token):
    """
    Log a user out of the system.

    :param token:   The ERP Loopback session token
    """
    try:
        # TODO: Call ERP API to log the user out
        pass
    except ResourceDoesNotExistException:
        raise ResourceDoesNotExistException('Session does not exist', internal_details=str(e))

    return


def get_token_for_user(auth_data, expire_days=None):
    """
    Generates an auth token for the given user.

    :param auth_data:     The auth data to be used for the token.
    :param expire_days:   The number of days until the token expires.
    :return:              A JSON Web Token.
    """

    # Generate token expiration data and add to dict
    exp = datetime.utcnow() + timedelta(days=expire_days)
    auth_data['exp'] = datetime.utcnow() + timedelta(days=expire_days)

    return tokenize(auth_data)


def get_auth_from_token(token):
    """
    Retrieve the Auth data associated with this token. May raise a
    TokenException if there are any issues parsing the token.

    :param token:  A JWT token that includes the Loopback token and user data
    :return:       An auth object.
    """
    data = detokenize(token)
    return data
