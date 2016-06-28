"""
The REST interface for ERP product resources.
"""
import server.services.products as product_service
from flask import g, Response, Blueprint
from server.web.utils import logged_in

products_v1_blueprint = Blueprint('products_v1_api', __name__)


@products_v1_blueprint.route('/products', methods=['GET'])
@logged_in
def get_products():
    """
    Get all product objects.

    :return: [{
        "id": "I9",
        "name": "Milk",
        "supplier": "Abbott"
    }, {...}]

    """

    products = product_service.get_products(token=g.auth['loopback_token'])
    return Response(products,
                    status=200,
                    mimetype='application/json')
