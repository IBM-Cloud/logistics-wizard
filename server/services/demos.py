"""
Handle all actions on the demo resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the demo
object and should just call into the service layer to act upon a demo resource.
"""
import requests
import json
from server.config import Config
from server.exceptions import (ResourceDoesNotExistException)
from server.exceptions import (ValidationException)

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


def find_user_in_demo(demo, user_id):
    """
    Finds a specific user within a demo object.

    :param demo:        An instance of the Demo model.
    :param user_id:     The user we are searching for.
    :return:            A dict representing the demo.
    """
    demo_users = json.loads(demo).get('users')
    for cur_user in demo_users:
        if cur_user.get('id') == user_id:
            return cur_user

    return


###########################
#         Services        #
###########################

def create_demo(demo_name, user_email):
    """
    Create a new demo session in the ERP system.

    :param demo_name:   Name of the demo being created.
    :param user_email:  Email of the user creating the demo.

    :return:         The created Demo model.
    """

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
    except ValidationException as e:
        raise ValidationException('ERP threw error creating new Demo', internal_details=str(e))

    # TODO: Send email to the user with demo info
    if user_email:
        pass

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
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('Demo does not exist', internal_details=str(e))
    except ValidationException as e:
        raise ValidationException('ERP threw error getting demo', internal_details=str(e))

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
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('Demo does not exist', internal_details=str(e))
    except ValidationException as e:
        raise ValidationException('ERP threw error deleting demo', internal_details=str(e))

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
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('Demo does not exist', internal_details=str(e))
    except ValidationException as e:
        raise ValidationException('ERP threw error retrieving retailers for demo',
                                  internal_details=str(e))

    return response.text
