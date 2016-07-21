"""
Handle all actions on the distribution center resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the distribution center
object and should just call into the service layer to act upon a distribution center resource.
"""
import requests
import json
from server.utils import get_service_url
from server.exceptions import (APIException,
                               AuthenticationException,
                               ResourceDoesNotExistException)

###########################
#         Utilities       #
###########################


def distribution_center_to_dict(distribution_center):
    """
    Convert an instance of the Distribution Center model to a dict.

    :param distribution_center: An instance of the Distribution Center model.
    :return:                    A dict representing the distribution center.
    """
    return {
        'id': distribution_center.id,
        'address': distribution_center.address,
        'contact': distribution_center.contact
    }


###########################
#         Services        #
###########################

def get_distribution_centers(token):
    """
    Get a list of distribution centers from the ERP system.

    :param token:   The ERP Loopback session token.

    :return:        The list of existing distribution centers.
    """

    # Create and format request to ERP
    url = '%s/api/v1/DistributionCenters' % get_service_url('lw-erp')
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving distribution centers', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def get_distribution_center(token, dc_id):
    """
    Get a distribution center from the ERP system.

    :param token:   The ERP Loopback session token.
    :param dc_id:   The ID of the distribution center to be retrieved.

    :return:        The retrieved distribution center.
    """

    # Create and format request to ERP
    url = '%s/api/v1/DistributionCenters/%s' % (get_service_url('lw-erp'), str(dc_id))
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving distribution center', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Distribution center does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def get_distribution_center_inventory(token, dc_id):
    """
    Get a distribution center from the ERP system.

    :param token:   The ERP Loopback session token.
    :param dc_id:   The ID of the distribution center for which inventory is to be be retrieved.

    :return:        The retrieved distribution center's inventory.
    """

    # Create and format request to ERP
    url = '%s/api/v1/DistributionCenters/%s/inventories' % (get_service_url('lw-erp'), str(dc_id))
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving distribution center inventory', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Distribution center does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text
