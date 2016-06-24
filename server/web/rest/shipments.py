"""
The REST interface for ERP shipment resources.
"""
import json

import server.services.shipments as shipment_service
from flask import g, request, Response, Blueprint
from server.web.utils import logged_in
from server.exceptions import (TokenException,
                               AuthorizationException,
                               ResourceDoesNotExistException,
                               ValidationException)
from server.web.utils import (get_json_data,
                              check_null_input)

shipments_v1_blueprint = Blueprint('shipments_v1_api', __name__)


@shipments_v1_blueprint.route('/shipments', methods=['GET'])
@logged_in
def get_shipments():
    """
    Get all shipment objects.

    :return: [{
        "id": "S5-51b8849982d82ea90d68b55f04be12b8",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "R2-51b8849982d82ea90d68b55f04be12b8"
    }, {...}]

    """

    status = request.args.get('status')
    shipments = shipment_service.get_shipments(token=g.auth['loopback_token'], status=status)
    return Response(shipments,
                    status=200,
                    mimetype='application/json')


@shipments_v1_blueprint.route('/shipments/<string:shipment_id>', methods=['GET'])
@logged_in
def get_shipment(shipment_id):
    """
    Retrieve a single shipment object.

    :param shipment_id:   The shipment's id

    :return: {
        "id": "S5-51b8849982d82ea90d68b55f04be12b8",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "R2-51b8849982d82ea90d68b55f04be12b8"
    }

    """
    check_null_input(shipment_id, 'a shipment to retrieve')

    shipment = shipment_service.get_shipment(token=g.auth['loopback_token'], shipment_id=shipment_id)
    return Response(shipment,
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
        "id": "S5-51b8849982d82ea90d68b55f04be12b8",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "R2-51b8849982d82ea90d68b55f04be12b8"
    }

    :return: {
        "id": "S5-51b8849982d82ea90d68b55f04be12b8",
        "status": "SHIPPED",
        "createdAt": "2015-11-05T22:00:51.692765",
        "updatedAt": "2015-11-08T22:00:51.692765",
        "deliveredAt": "2015-11-08T22:00:51.692765",
        "estimatedTimeOfArrival": "2015-11-07T22:00:51.692765",
        "currentLocation": {Address},
        "fromId": "D2",
        "toId:": "R2-51b8849982d82ea90d68b55f04be12b8"
    }

    """
    check_null_input(shipment_id, 'a shipment to update')

    updated_shipment = get_json_data(request)
    shipment = shipment_service.update_shipment(token=g.auth['loopback_token'],
                                                shipment_id=shipment_id, shipment=updated_shipment)
    return Response(shipment,
                    status=200,
                    mimetype='application/json')
