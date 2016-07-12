"""
The REST interface for ERP distribution center resources.
"""
import json

import server.services.distribution_centers as distribution_center_service
from flask import g, request, Response, Blueprint
from server.web.utils import logged_in
from server.exceptions import (TokenException,
                               AuthorizationException,
                               ResourceDoesNotExistException,
                               ValidationException)
from server.web.utils import (get_json_data,
                              check_null_input)

distribution_centers_v1_blueprint = Blueprint('distribution_centers_v1_api', __name__)


@distribution_centers_v1_blueprint.route('/distribution-centers', methods=['GET'])
@logged_in
def get_distribution_centers():
    """
    Get all distribution center objects.

    :return: [{
        "id": "D2",
        "address": {Address},
        "contact": {Contact}
    }, {...}]

    """

    distribution_centers = distribution_center_service.get_distribution_centers(token=g.auth['loopback_token'])
    return Response(distribution_centers,
                    status=200,
                    mimetype='application/json')


@distribution_centers_v1_blueprint.route('/distribution-centers/<string:dc_id>', methods=['GET'])
@logged_in
def get_distribution_center(dc_id):
    """
    Retrieve a single distribution center object.

    :param dc_id:   The distribution center's id

    :return: {
        "id": "D2",
        "address": {Address},
        "contact": {Contact}
    }

    """
    check_null_input(dc_id, 'a distribution center to retrieve')

    distribution_center = distribution_center_service.get_distribution_center(token=g.auth['loopback_token'],
                                                                              dc_id=dc_id)
    return Response(distribution_center,
                    status=200,
                    mimetype='application/json')


@distribution_centers_v1_blueprint.route('/distribution-centers/<string:dc_id>/inventory', methods=['GET'])
@logged_in
def get_distribution_center_inventory(dc_id):
    """
    Retrieve all inventory at the specified distribution center.

    :param dc_id:   The distribution center's id

    :return: [{
        "id": "123",
        "quantity": 10,
        "productId": "123",
        "locationId": "123",
        "locationType": "DistributionCenter"
    }, {...}]
    """
    check_null_input(dc_id, 'a distribution center whose inventory you want to retrieve')

    inventory = distribution_center_service.get_distribution_center_inventory(token=g.auth['loopback_token'],
                                                                              dc_id=dc_id)
    return Response(inventory,
                    status=200,
                    mimetype='application/json')
