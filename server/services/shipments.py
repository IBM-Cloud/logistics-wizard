"""
Handle all actions on the shipment resource and is responsible for making sure
the calls get routed to the ERP service appropriately. As much as possible,
the interface layer should have no knowledge of the properties of the shipment
object and should just call into the service layer to act upon a shipment resource.
"""
import requests
import json
from server.utils import get_service_url
from server.exceptions import (APIException,
                               AuthenticationException,
                               UnprocessableEntityException,
                               ResourceDoesNotExistException,
                               ValidationException)

###########################
#         Utilities       #
###########################


def shipment_to_dict(shipment):
    """
    Convert an instance of the Shipment model to a dict.

    :param shipment:  An instance of the Shipment model.
    :return:      A dict representing the shipment.
    """
    return {
        'id': shipment.id,
        'status': shipment.status,
        'createdAt': shipment.createdAt,
        'updatedAt': shipment.updatedAt,
        'deliveredAt': shipment.deliveredAt,
        'estimatedTimeOfArrival': shipment.estimatedTimeOfArrival,
        'currentLocation': shipment.currentLocation,
        'fromId': shipment.fromId,
        'toId': shipment.toId
    }


def add_query_filter(cur_query, filter_type, op, value, property_name=None):
    """
    Add a query condition to an input query string

    :param cur_query:       The current query string.
    :param filter_type:     The type of Loopback filter for the query.
    :param property_name:   The object's property used by the query to filter the result set.
    :param op:              Equivalence operator for the query's evaluation.
    :param value:           The value that the property is evaluated against.

    :return:         The list of existing shipments.
    """

    # If the query string is null, initialize it
    # If it is non-empty, separate from new query with ampersand
    if cur_query is None or cur_query == "":
        cur_query = "?"
    else:
        cur_query += "&"

    cur_query += "filter[" + filter_type + "]"
    if property_name is not None:
        cur_query += "[" + property_name + "]"
    return cur_query + op + str(value)


###########################
#         Services        #
###########################

def get_shipments(token, retailer_id=None, dc_id=None, status=None):
    """
    Get a list of shipments from the ERP system.

    :param token:       The ERP Loopback session token.
    :param status:      Status of the shipments to be retrieved.
    :param retailer_id: Retailer of the shipments to be retrieved.
    :param dc_id:       Distribution center of the shipments to be retrieved.

    :return:         The list of existing shipments.
    """

    # Add filters if corresponding inputs are present
    status_query = ""
    if status is not None:
        status_query = add_query_filter(status_query, "where", "=", status, property_name="status")
    if retailer_id is not None:
        status_query = add_query_filter(status_query, "where", "=", retailer_id, property_name="toId")
    if dc_id is not None:
        status_query = add_query_filter(status_query, "where", "=", dc_id, property_name="fromId")

    # Create and format request to ERP
    url = '%s/api/v1/Shipments%s' % (get_service_url('lw-erp'), status_query)
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving shipments', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def get_shipment(token, shipment_id, include_items=None):
    """
    Get a shipment from the ERP system.

    :param token:           The ERP Loopback session token.
    :param shipment_id:     The ID of the shipment to be retrieved.
    :param include_items:   Indicates if items are to be returned with shipment.

    :return:         The retrieved shipment.
    """

    # Add filters if corresponding inputs are present
    status_query = ""
    if include_items != "0":
        status_query = add_query_filter(status_query, "include", "=", "items")

    # Create and format request to ERP
    url = '%s/api/v1/Shipments/%s%s' % (get_service_url('lw-erp'), str(shipment_id), status_query)
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error retrieving shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Shipment does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def create_shipment(token, shipment):
    """
    Create a shipment in the ERP system.

    :param token:       The ERP Loopback session token.
    :param shipment:    The shipment object to be created.

    :return:         The created shipment.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Shipments' % get_service_url('lw-erp')
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'Authorization': token
    }
    shipment_json = json.dumps(shipment)

    try:
        response = requests.request("POST", url, data=shipment_json, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error creating shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 400:
        raise ValidationException('Bad shipment data',
                                  internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 422:
        raise UnprocessableEntityException('Required data for shipment is either absent or invalid',
                                           internal_details=json.loads(response.text).get('error').get('message'))

    return response.text


def delete_shipment(token, shipment_id):
    """
    Delete a shipment from the ERP system.

    :param token:       The ERP Loopback session token.
    :param shipment_id: The ID of the shipment to be deleted.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Shipments/%s' % (get_service_url('lw-erp'), str(shipment_id))
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("DELETE", url, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error deleting shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Shipment does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return


def update_shipment(token, shipment_id, shipment):
    """
    Update a shipment from the ERP system.

    :param token:       The ERP Loopback session token.
    :param shipment_id: The ID of the shipment to be retrieved.
    :param shipment:    The shipment object with values to update.

    :return:         The updated shipment.
    """

    # Create and format request to ERP
    url = '%s/api/v1/Shipments/%s' % (get_service_url('lw-erp'), str(shipment_id))
    headers = {
        'cache-control': "no-cache",
        'Authorization': token
    }

    try:
        response = requests.request("PUT", url, data=shipment, headers=headers)
    except Exception as e:
        raise APIException('ERP threw error updating shipment', internal_details=str(e))

    # Check for possible errors in response
    if response.status_code == 400:
        raise ValidationException('Invalid update to shipment',
                                  internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 401:
        raise AuthenticationException('ERP access denied',
                                      internal_details=json.loads(response.text).get('error').get('message'))
    elif response.status_code == 404:
        raise ResourceDoesNotExistException('Shipment does not exist',
                                            internal_details=json.loads(response.text).get('error').get('message'))

    return response.text
