"""
The REST interface for demo session resources.
"""
import json

import server.services.demos as demo_service
import server.services.users as user_service
import server.services.shipments as shipment_service
import server.services.distribution_centers as distribution_center_service
import server.services.retailers as retailer_service
from flask import g, request, Response, Blueprint
from multiprocessing import Pool
from server.exceptions import (TokenException,
                               ResourceDoesNotExistException,
                               APIException)
from server.utils import async_helper
from server.web.utils import (get_token_from_request,
                              get_json_data,
                              check_null_input,
                              logged_in)

demos_v1_blueprint = Blueprint('demos_v1_api', __name__)


def setup_auth_from_request():
    """
    Get the Auth data from the request headers and store on the g
    object for later use.
    """
    try:
        token = get_token_from_request()
        if token is not None:
            g.auth = user_service.get_auth_from_token(token)
    except (TokenException, ResourceDoesNotExistException):
        g.auth = None


@demos_v1_blueprint.route('/demos', methods=['POST'])
def create_demo():
    """
    Create a new demo resource.

    :param {
        "name": "Example Demo Name",
        "email": "test@example.com"
    }

    :return: {
        "id": "123",
        "name": "Example Demo Name",
        "guid": "JDJhJDEdTRUR...VBrbW9vcj3k4L2sy",
        "createdAt": "2015-11-05T22:00:51.692765",
        "users": [{User}...{User}]
    }

    """

    # Get inputs and make sure required params are not null
    data = get_json_data(request)
    demo_name = data.get('name')
    user_email = data.get('email')
    check_null_input(demo_name, 'a demo name for the new demo session')

    demo = demo_service.create_demo(demo_name, user_email)
    return Response(demo,
                    status=201,
                    mimetype='application/json')


@demos_v1_blueprint.route('/demos/<string:guid>', methods=['GET'])
def get_demo(guid):
    """
    Retrieve a single demo object.

    :param guid:   The demo's guid

    :return: {
        "id": "123",
        "name": "Example Demo Name",
        "guid": "JDJhJDEdTRUR...VBrbW9vcj3k4L2sy",
        "createdAt": "2015-11-05T22:00:51.692765",
        "users": [{User}...{User}]
    }
    """
    check_null_input(guid, 'a demo to retrieve')

    demo = demo_service.get_demo_by_guid(guid)
    return Response(demo,
                    status=200,
                    mimetype='application/json')


@demos_v1_blueprint.route('/demos/<string:guid>', methods=['DELETE'])
def delete_demo(guid):
    """
    Delete a demo object and all its children.

    :param guid:   The demo's guid
    :return:
    """
    check_null_input(guid, 'a demo to delete')

    demo_service.delete_demo_by_guid(guid)
    return '', 204


@demos_v1_blueprint.route('/demos/<string:guid>/retailers', methods=['GET'])
def get_demo_retailers(guid):
    """
    Retrieve a single demo's list of retailers.

    :param guid:   The demo's guid

    :return: [{
        "id": "123",
        "address": {
          "city": "Raleigh",
          "state": "North Carolina",
          "country": "US",
          "latitude": 35.71,
          "longitude": -78.63
        },
        "managerId": "123"
    }, {...}]
    """
    check_null_input(guid, 'a demo for which to retrieve retailers')

    retailers = demo_service.get_demo_retailers(guid)
    return Response(retailers,
                    status=200,
                    mimetype='application/json')


@demos_v1_blueprint.route('/demos/<string:guid>/users', methods=['POST'])
def create_demo_user(guid):
    """
    Create a new user for a single demo

    :param guid:   The demo's guid
    :param {
        "retailerId": "123"
    }

    :return: {
        "id": "123",
        "demoId": "123",
        "username": "Retail Store Manager (XXX)",
        "email": "ruth.XXX@acme.com"
    }
    """

    # Get inputs and make sure required params are not null
    data = get_json_data(request)
    retailer_id = data.get('retailerId')
    check_null_input(guid, 'a demo for which to create a user')
    check_null_input(retailer_id, 'a retailer to make a user for the demo')

    user = user_service.create_user(guid, retailer_id)
    return Response(user,
                    status=201,
                    mimetype='application/json')


"""
@demos_v1_blueprint.route('/demos/<string:guid>/users/<string:user_id>', methods=['GET'])
def get_demo_user(guid, user_id):

    Gets a user of a single demo

    :param guid:   The demo's guid
    :param user_id:   The user being retrieved

    :return: {
        "id": "123",
        "demoId": "123",
        "username": "Retail Store Manager (XXX)",
        "email": "ruth.XXX@acme.com"
    }

    if guid is None:
        raise ValidationException('You must specify a demo for which to retrieve a user')
    if user_id is None:
        raise ValidationException('You must specify a user ID to retrieve')

    user = user_service.get_user_by_id(guid, user_id)
    return Response(jsonify(user, user_service.user_to_dict),
                    status=200,
                    mimetype='application/json')
"""


@demos_v1_blueprint.route('/demos/<string:guid>/login', methods=['POST'])
def demo_login(guid):
    """
    Login to a demo as a specific user

    :param {
        "userId": "123"
    }

    :return: {
        "token": "eyJhbGciOi...WT2aGgjY5JHvCsbA"
    }
    """
    data = request.get_json()
    user_id = data.get('userId')
    check_null_input(user_id, 'a username when logging in')
    check_null_input(guid, 'a demo guid when logging in')

    # Login through the ERP system and create a JWT valid for 2 weeks
    auth_data = user_service.login(guid, user_id)
    token = user_service.get_token_for_user(auth_data, expire_days=14)
    resp = Response(json.dumps({'token': token}),
                    status=200,
                    mimetype='application/json')

    resp.set_cookie('auth_token', token, httponly=True)
    return resp


@demos_v1_blueprint.route('/logout/<string:token>', methods=['DELETE'])
def deauthenticate(token):
    """
    Logout the current user
    :param token  Current web token
    :return:
    """
    request_token = get_token_from_request()
    # Only allow deletion of a web token if the token belongs to the current user
    if request_token == token:
        user_service.logout(token=g.auth['loopback_token'])
    return '', 204


@demos_v1_blueprint.route('/admin', methods=['GET'])
@logged_in
def load_admin_data():
    """
    Load all data relative to the currently logged in user

    :return: {
        "shipments": [{Shipments}],
        "retailers": [{Retailer}],
        "distribution_centers": [{Distribution Center}]
    }
    """

    # Specify functions and corresponding arguments to call to retrieve ERP data
    loopback_token = g.auth['loopback_token']
    erp_calls = [(shipment_service.get_shipments, loopback_token),
                 (distribution_center_service.get_distribution_centers, loopback_token),
                 (retailer_service.get_retailers, loopback_token)]
    pool = Pool(processes=len(erp_calls))

    # Asynchronously make calls and then wait on all processes to finish
    try:
        results = pool.map(async_helper, erp_calls)
    except Exception as e:
        raise APIException('Error retrieving admin data view', internal_details=str(e))

    pool.close()
    pool.join()
    # Send back serialized results to client
    return Response(json.dumps({
                        "shipments": json.loads(results[0]),
                        "distribution-centers": json.loads(results[1]),
                        "retailers": json.loads(results[2])
                    }),
                    status=200,
                    mimetype='application/json')
