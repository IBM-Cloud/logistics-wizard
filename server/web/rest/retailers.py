"""
The REST interface for ERP retailer resources.
"""
import json

import server.services.retailers as retailer_service
from flask import g, request, Response, Blueprint
from server.web.utils import logged_in
from server.exceptions import (TokenException,
                               AuthorizationException,
                               ResourceDoesNotExistException,
                               ValidationException)
from server.web.utils import (get_json_data,
                              check_null_input)

retailers_v1_blueprint = Blueprint('retailers_v1_api', __name__)


@retailers_v1_blueprint.route('/retailers', methods=['GET'])
@logged_in
def get_retailers():
    """
    Get all retailer objects.

    :return: [{
        "id": "R1-331ba1af395808e6fddf3466fe218485",
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
    Retrieve a single distribution center object.

    :param retailer_id:   The retailer's id

    :return: {
        "id": "D2",
        "address": {Address}
    }

    """
    check_null_input(retailer_id, 'a retailer to retrieve')

    retailer = retailer_service.get_retailer(token=g.auth['loopback_token'],
                                                        retailer_id=retailer_id)
    return Response(retailer,
                    status=200,
                    mimetype='application/json')
