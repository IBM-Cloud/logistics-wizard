"""
Handle all actions on the demo resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the demo
object and should just call into the service layer to act upon a demo resource.
"""
from server.config import Config
from server.exceptions import (ResourceDoesNotExistException)


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
        'id': demo.get('id'),
        'name': demo.get('name'),
        'guid': demo.get('guid'),
        'createdAt': demo.get('createdAt'),
        'users': demo.get('users')
    }


###########################
#         Services        #
###########################

def create_demo(demo_name, user_email):
    """
    Create a new demo session in the ERP system.

    :return:         The created Demo model.
    """
    # TODO: Call ERP API to create a demo
    users = list()
    users.append({
        'id': "123",
        'email': "test@example.com",
        'username': "test@example.com",
        'role': "supplychainmanager",
        'createdAt': "2015-11-05T22:00:51.692765"
    })
    demo = {
        'id': "123",
        'name': demo_name,
        'guid': "JDJhJDEdTRURVBrbW9vcj3k4L2sy",
        'createdAt': "2015-11-05T22:00:51.692765",
        'users': users
    }

    # TODO: Send email to the user with demo info
    if user_email:
        pass

    return demo


def get_demo_by_guid(guid):
    """
    Retrieve a demo from the ERP system by guid.

    :param guid:    The demo's guid.
    :return:        An instance of the Demo.
    """
    try:
        # TODO: Call ERP API to get the demo
        users = list()
        users.append({
            'id': "123",
            'email': "test@example.com",
            'username': "test@example.com",
            'role': "supplychainmanager",
            'createdAt': "2015-11-05T22:00:51.692765"
        })
        demo = {
            'id': "123",
            'guid': guid,
            'createdAt': "2015-11-05T22:00:51.692765",
            'users': users
        }
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('Demo does not exist', internal_details=str(e))
    return demo


def delete_demo_by_guid(guid):
    """
    Delete a demo from the ERP system by guid.

    :param guid:    The demo's guid.
    """
    try:
        # TODO: Call ERP API to delete the demo
        pass
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('Demo does not exist', internal_details=str(e))
    return


def get_demo_retailers(guid):
    """
    Retrieve retailers for a demo in the ERP system by guid.

    :param guid:    The demo's guid.
    :return:        An instance of the Demo.
    """
    try:
        # TODO: Call ERP API to get the demo retailers
        retailers = list()
        contact = {
            'id': "123",
            'name': "John Smith"
        }
        address = {
            'city': "New York City",
            'state': "New York",
            'country': "United States",
            'latitude': "123.1234",
            'longitude': "123.1234",
            'id': "123",
        }
        retailers.append({
            'id': "123",
            'contact': contact,
            'address': address
        })
        retailers.append({
            'id': "321",
            'contact': contact,
            'address': address
        })
    except ResourceDoesNotExistException as e:
        raise ResourceDoesNotExistException('Demo does not exist', internal_details=str(e))
    return retailers
