"""
Handle all actions on the user resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the user
object and should just call into the service layer to act upon a user resource.
"""
from datetime import datetime, timedelta
import json
import requests

import server.services.demos as demo_service
from server.config import Config
from server.exceptions import (ResourceDoesNotExistException,
                               AuthenticationException,
                               APIException,
                               ValidationException)
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
        'id': user.id,
        'demoId': user.demoId,
        'email': user.email,
        'username': user.username,
        'roles': user.roles
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

    # Create and format request to ERP
    url = Config.ERP + "Demos/" + guid + "/createUser"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    payload = dict()
    payload['retailerId'] = int(retailer_id)
    payload_json = json.dumps(payload)

    try:
        response = requests.request("POST", url, data=payload_json, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error creating new user for demo', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 404:
        raise ResourceDoesNotExistException('Demo or retailer does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


"""
def get_user_by_id(guid, user_id):

    Retrieve a user from the ERP system by user_id.

    :param guid:        The demo's guid
    :param user_id:   The user's id.
    :return:          An instance of the User.

    try:
        # TODO: Waiting for ERP API to implement this
        roles = list()
        roles.append({
            "id": "2",
            "name": "retailstoremanager",
            "created": "2016-05-30T18:32:50.077Z",
            "modified": "2016-05-30T18:32:50.077Z"
        })
        user = {
            'id': user_id,
            "demoId": "123",
            'email': "test@example.com",
            'username': "Retail Store Manager (test)",
            'roles': roles
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('User does not exist', internal_details=str(e))
    except ValidationException as e:
        raise ValidationException('ERP threw error retrieving the user',
                                  internal_details=str(e))
    return user
"""


def login(guid, user_id):
    """
    Authenticate a user against the ERP system.

    :param guid:        The demo guid being logged in for.
    :param user_id:     The user_id for which to log in.
    :return:            Auth data returned by ERP system
    """

    # Create and format request to ERP
    url = Config.ERP + "Demos/" + guid + "/loginAs"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    payload = dict()
    payload['userId'] = int(user_id)
    payload_json = json.dumps(payload)

    try:
        response = requests.request("POST", url, data=payload_json, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error creating new user for demo', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 404:
        raise ResourceDoesNotExistException('Demo or user does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    login_response = json.loads(response.text)
    return {
        'loopback_token': login_response.get('token').get('id'),
        'user': login_response.get('user')
    }


def logout(token):
    """
    Log a user out of the system.

    :param token:   The ERP Loopback session token
    """

    # Create and format request to ERP
    url = Config.ERP + "Users/logout"
    headers = {
        'content-type': "application/json",
        'Authorization': token
    }

    try:
        response = requests.request("POST", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error creating new user for demo', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 500:
        raise ResourceDoesNotExistException('Session does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

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
