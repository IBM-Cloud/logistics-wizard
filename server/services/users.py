"""
Handle all actions on the user resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the user
object and should just call into the service layer to act upon a user resource.
"""
import json
import requests
from server.utils import get_service_url
from server.exceptions import ResourceDoesNotExistException, APIException


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
    url = '%s/api/v1/Demos/%s/createUser' % (get_service_url('lw-erp'), guid)
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


def login(guid, user_id):
    """
    Authenticate a user against the ERP system.

    :param guid:        The demo guid being logged in for.
    :param user_id:     The user_id for which to log in.
    :return:            Auth data returned by ERP system
    """

    # Create and format request to ERP
    url = '%s/api/v1/Demos/%s/loginAs' % (get_service_url('lw-erp'), guid)
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
    url = '%s/api/v1/Users/logout' % get_service_url('lw-erp')
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
