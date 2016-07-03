"""
Handle all actions on the demo resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the demo
object and should just call into the service layer to act upon a demo resource.
"""
import requests
import json
import server.services.messaging as messaging_service
from server.config import Config
from server.utils import validate_email
from server.exceptions import (ResourceDoesNotExistException)
from server.exceptions import (APIException,
                               ValidationException,
                               UnprocessableEntityException)

###########################
#         Utilities       #
###########################


def demo_to_dict(demo):
    """
    Convert an instance of the Demo model to a dict.

    :param demo:  An instance of the Demo model.
    :return:      A dict representing the demo.
    """
    return {
        'id': demo.id,
        'name': demo.name,
        'guid': demo.guid,
        'createdAt': demo.createdAt,
        'users': demo.users
    }


###########################
#         Services        #
###########################

def create_demo(demo_name, user_email=None):
    """
    Create a new demo session in the ERP system.

    :param demo_name:   Name of the demo being created.
    :param user_email:  Email of the user creating the demo.

    :return:         The created Demo model.
    """

    # Check email
    if user_email is not None and validate_email(user_email) == False:
        raise UnprocessableEntityException("Invalid email address")

    # Create and format request to ERP
    url = Config.ERP + "Demos"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    payload = dict()
    payload['name'] = demo_name
    payload_json = json.dumps(payload)

    try:
        response = requests.request("POST", url, data=payload_json, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error creating new Demo', internal_details=str(e))

    if user_email:
        demo = json.loads(response.text)
        subject = "Your Logistics Wizard session has been created - Demo #" + \
                  demo.get('guid')[-6:].upper()
        message = messaging_service.compose_welcome_msg(demo.get('guid'), demo.get('users')[0])
        messaging_service.send_email(user_email, subject, message, 'html')

    return response.text


def get_demo_by_guid(guid):
    """
    Retrieve a demo from the ERP system by guid.

    :param guid:    The demo's guid.

    :return:        An instance of the Demo.
    """

    # Create and format request to ERP
    url = Config.ERP + "Demos/findByGuid/" + guid
    headers = {
        'cache-control': "no-cache"
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving demo', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 404:
        raise ResourceDoesNotExistException('Demo does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def delete_demo_by_guid(guid):
    """
    Delete a demo from the ERP system by guid.

    :param guid:    The demo's guid.
    """

    # Create and format request to ERP
    url = Config.ERP + "Demos/" + guid

    try:
        response = requests.request("DELETE", url)
    except Exception as e:
        raise APIException('ERP threw error deleting demo', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 404:
        raise ResourceDoesNotExistException('Demo does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return


def get_demo_retailers(guid):
    """
    Retrieve retailers for a demo in the ERP system by guid.

    :param guid:    The demo's guid.
    :return:        An instance of the Demo.
    """

    # Create and format request to ERP
    url = Config.ERP + "Demos/" + guid + "/retailers"
    headers = {
        'cache-control': "no-cache"
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving retailers for demo',
                           internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 404:
        raise ResourceDoesNotExistException('Demo does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text
