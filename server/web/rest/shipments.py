"""
The REST interface for ERP shipment resources.
"""
import json

import server.services.shipments as shipment_service
from flask import g, request, Response, Blueprint
from multiprocessing import Pool
from server.web.utils import logged_in
from server.utils import async_helper
from server.web.utils import (get_json_data,
                              check_null_input)
from server.exceptions import APIException

shipments_v1_blueprint = Blueprint('shipments_v1_api', __name__)


@shipments_v1_blueprint.route('/shipments', methods=['GET'])
@logged_in
def get_shipments():
    """
    Get all shipment objects.

    :return: [{
        "id": "123",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "123"
    }, {...}]

    """

    status = request.args.get('status')
    retailer_id = request.args.get('rid')
    dc_id = request.args.get('did')
    shipments = shipment_service.get_shipments(token=g.auth['loopback_token'],
                                               status=status,
                                               retailer_id=retailer_id,
                                               dc_id=dc_id)
    return Response(shipments,
                    status=200,
                    mimetype='application/json')


@shipments_v1_blueprint.route('/shipments', methods=['POST'])
@logged_in
def create_shipment():
    """
    Create a new shipment object.

    :param {
        "status": "NEW",
        "estimatedTimeOfArrival": "2016-07-10T00:00:00.000Z",
        "fromId": "D2",
        "toId": "123"
    }

    :return: {
        "id": "123",
        "status": "ACCEPTED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2016-07-10T00:00:00.000Z",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "123"
    }

    """

    # Get inputs and make sure required params are not null
    data = get_json_data(request)

    shipment = shipment_service.create_shipment(token=g.auth['loopback_token'], shipment=data)
    return Response(shipment,
                    status=201,
                    mimetype='application/json')


@shipments_v1_blueprint.route('/shipments/<string:shipment_id>', methods=['GET'])
@logged_in
def get_shipment(shipment_id):
    """
    Retrieve a single shipment object.

    :param shipment_id:   The shipment's id

    :return: {
        "id": "123",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "123",
        "toId:": "123",
        "items": [{LineItem}]
    }

    """
    include_items = request.args.get('include_items')
    check_null_input(shipment_id, 'a shipment to retrieve')

    # Set up calls to retrieve shipment data based on inputs
    loopback_token = g.auth['loopback_token']
    erp_calls = [(shipment_service.get_shipment, loopback_token, shipment_id)]
    if include_items != "0":
        erp_calls.append((shipment_service.get_shipment_items, loopback_token, shipment_id))
    pool = Pool(processes=len(erp_calls))

    # Asynchronously make calls and then wait on all processes to finish
    try:
        results = [json.loads(x) for x in pool.map(async_helper, erp_calls)]
    except Exception as e:
        raise APIException('Error retrieving shipment data', internal_details=str(e))
    pool.close()
    pool.join()

    # Retrieve results from ERP calls and return shipment object
    shipment = results[0]
    if len(results) > 1:
        shipment['items'] = results[1]

    return Response(json.dumps(shipment),
                    status=200,
                    mimetype='application/json')


@shipments_v1_blueprint.route('/shipments/<string:shipment_id>', methods=['DELETE'])
@logged_in
def delete_shipment(shipment_id):
    """
    Retrieve a single shipment object.

    :param shipment_id:   The shipment's id
    :return:

    """
    check_null_input(shipment_id, 'a shipment to delete')

    shipment_service.delete_shipment(token=g.auth['loopback_token'], shipment_id=shipment_id)
    return '', 204


@shipments_v1_blueprint.route('/shipments/<string:shipment_id>', methods=['PUT'])
@logged_in
def update_shipment(shipment_id):
    """
    Update a single shipment object.

    :param shipment_id:   The shipment's id
    :param  {
        "id": "123",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "123"
    }

    :return: {
        "id": "123",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "123"
    }

    """
    check_null_input(shipment_id, 'a shipment to update')

    updated_shipment = get_json_data(request)
    shipment = shipment_service.update_shipment(token=g.auth['loopback_token'],
                                                shipment_id=shipment_id, shipment=updated_shipment)
    return Response(shipment,
                    status=200,
                    mimetype='application/json')
