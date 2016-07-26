"""
The REST interface for ERP retailer resources.
"""
import server.services.retailers as retailer_service
import server.services.shipments as shipment_service
from flask import g, request, Response, Blueprint
from server.web.utils import logged_in, check_null_input

retailers_v1_blueprint = Blueprint('retailers_v1_api', __name__)


@retailers_v1_blueprint.route('/retailers', methods=['GET'])
@logged_in
def get_retailers():
    """
    Get all retailer objects.

    :return: [{
        "id": "123",
        "address": {Address}
    }, {...}]

    """

    retailers = retailer_service.get_retailers(token=g.auth['loopback_token'])
    return Response(retailers,
                    status=200,
                    mimetype='application/json')


@retailers_v1_blueprint.route('/retailers/<string:retailer_id>', methods=['GET'])
@logged_in
def get_retailer(retailer_id):
    """
    Retrieve a single retailer object.

    :param retailer_id:   The retailer's id

    :return: {
        "id": "123",
        "address": {Address}
    }

    """
    check_null_input((retailer_id, 'retailer to retrieve'))

    retailer = retailer_service.get_retailer(token=g.auth['loopback_token'],
                                             retailer_id=retailer_id)
    return Response(retailer,
                    status=200,
                    mimetype='application/json')


@retailers_v1_blueprint.route('/retailers/<string:retailer_id>/shipments', methods=['GET'])
@logged_in
def get_retailer_shipments(retailer_id):
    """
    Retrieve all shipments heading to the specified retailer.

    :param retailer_id:   The retailer's id

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
    check_null_input((retailer_id, 'retailer whose shipments you want to retrieve'))
    status = request.args.get('status')

    shipments = shipment_service.get_shipments(token=g.auth['loopback_token'],
                                               retailer_id=retailer_id,
                                               status=status)
    return Response(shipments,
                    status=200,
                    mimetype='application/json')


@retailers_v1_blueprint.route('/retailers/<string:retailer_id>/inventory', methods=['GET'])
@logged_in
def get_retailer_inventory(retailer_id):
    """
    Retrieve all inventory at the specified retailer.

    :param retailer_id:   The retailer's id

    :return: [{
        "id": "123",
        "quantity": 10,
        "productId": "123",
        "locationId": "123",
        "locationType": "Retailer"
    }, {...}]
    """
    check_null_input((retailer_id, 'retailer whose inventory you want to retrieve'))

    inventory = retailer_service.get_retailer_inventory(token=g.auth['loopback_token'],
                                                        retailer_id=retailer_id)
    return Response(inventory,
                    status=200,
                    mimetype='application/json')
