"""
Handle all actions on the retailer resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the retailer
object and should just call into the service layer to act upon a retailer resource.
"""
import requests
import json
from server.utils import get_service_url
from server.exceptions import (ResourceDoesNotExistException)
from server.exceptions import (APIException,
                               AuthenticationException,
                               UnprocessableEntityException)

###########################
#         Utilities       #
###########################


def retailer_to_dict(retailer):
    """
    Convert an instance of the Retailer model to a dict.

    :param retailer:  An instance of the Retailer model.
    :return:      A dict representing the retailer.
    """
    return {
        'id': retailer.id,
        'address': retailer.address
    }


###########################
#         Services        #
###########################

def get_retailers(token):
    """
    Get a list of retailers from the ERP system.

    :param token:   The ERP Loopback session token.

    :return:        The list of existing retailers.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Retailers' % get_service_url('lw-erp')
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving retailers', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def get_retailer(token, retailer_id):
    """
    Get a retailer from the ERP system.

    :param token:       The ERP Loopback session token.
    :param retailer_id: The ID of the retailer to be retrieved.

    :return:        The retrieved retailer.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Retailers/%s' % (get_service_url('lw-erp'), str(retailer_id))
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving retailer', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Retailer does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def get_retailer_inventory(token, retailer_id):
    """
    Get a retailer from the ERP system.

    :param token:       The ERP Loopback session token.
    :param retailer_id: The ID of the retailer for which inventory is to be be retrieved.

    :return:        The retrieved retailer's inventory.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Retailers/%s/inventories' % (get_service_url('lw-erp'), str(retailer_id))
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving retailer inventory', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Retailer does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text
