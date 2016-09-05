"""
The REST interface for the root API
"""
from flask import Response, Blueprint

root_v1_blueprint = Blueprint('root_v1_api', __name__)

@root_v1_blueprint.route('/', methods=['GET'])
def ping():
    """
    Return a health status.

    :return: {
        "status": "OK"
    }

    """

    return Response('{"status": "OK"}',
                    status=200,
                    mimetype='application/json')