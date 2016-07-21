"""
Handle all actions on the product resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the product
object and should just call into the service layer to act upon a product resource.
"""
import requests
import json
from server.utils import get_service_url
from server.exceptions import (APIException,
                               AuthenticationException)

###########################
#         Utilities       #
###########################


def product_to_dict(product):
    """
    Convert an instance of the Product model to a dict.

    :param product: An instance of the Product model.
    :return:        A dict representing the product.
    """
    return {
        'id': product.id,
        'name': product.name,
        'supplierId': product.supplierId
    }


###########################
#         Services        #
###########################

def get_products(token):
    """
    Get a list of products from the ERP system.

    :param token:   The ERP Loopback session token.

    :return:        The list of existing products.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Products' % get_service_url('lw-erp')
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving products', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))

    return response.text
