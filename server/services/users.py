"""
Handle all actions on the user resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the user
object and should just call into the service layer to act upon a user resource.
"""
from datetime import datetime, timedelta

from server.exceptions import (TokenException,
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
        'id': user.get('id'),
        'email': user.get('email'),
        'username': user.get('username'),
        'role': user.get('role'),
        'createdAt': user.get('createdAt')
    }


###########################
#         Services        #
###########################


def create_user(guid, retailer_id):
    """
    Create a new user in the ERP system.

    :param guid:        The demo's guid
    :param retailer_id: Retailer the user will be associated with.

    :return:            The created User model.
    """
    # TODO: Call ERP API to create a user
    user = {
        'id': "123",
        'email': "test@example.com",
        'username': "test@example.com",
        'role': "retailstoremanager",
        'createdAt': "2015-11-05T22:00:51.692765"
    }

    return user


def get_user_by_id(guid, user_id):
    """
    Retrieve a user from the ERP system by user_id.

    :param guid:        The demo's guid
    :param user_id:   The user's id.
    :return:          An instance of the User.
    """
    try:
        # TODO: Call ERP API to get the user
        user = {
            'id': "123",
            'email': "test@example.com",
            'username': "test@example.com",
            'role': "retailstoremanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('User does not exist', internal_details=str(e))
    return user


def login(guid, user_id):
    """
    Authenticate a user against the ERP system.

    :param guid:        The demo guid being logged in for.
    :param user_id:     The user_id for which to log in.
    :return:            Auth data returned by ERP system
    """
    try:
        # TODO: Call ERP API to log the user in
        auth_data = {
            'id': "UQO8hEw5tSc4LBPuRDZ7fmUyiqgZPH5o0XhEla29PAr8d7D0OEfRYYo5gCBoHm9b",
            'ttl': 1209600,
            'created': "2016-05-30T21:56:43.727Z",
            'userId': user_id
        }
    except ResourceDoesNotExistException:
        raise AuthenticationException('User does not exist')

    user = get_user_by_id(guid, user_id)

    return {
        'loopback_token': auth_data.get('id'),
        'user': user
    }


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
