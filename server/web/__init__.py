"""
Initializer for the API application. This will create a new Flask app and
register all interface versions (Blueprints), initialize the database and
register app level error handlers.
"""
import re
import json

from flask import Flask, current_app, Response
from flask.ext.cors import CORS
from server.web.utils import compose_error


def create_app():
    """
    Create the api as it's own app so that it's easier to scale it out on it's
    own in the future.

    :return:         A flask object/wsgi callable.
    """
    from server.config import Config
    from server.exceptions import APIException
    from server.web.utils import request_wants_json
    from server.web.rest.demos import demos_v1_blueprint, setup_auth_from_request

    # Create the app
    logistics_wizard = Flask('logistics_wizard', static_folder=None)
    CORS(logistics_wizard, origins=[re.compile('.*')], supports_credentials=True)
    if Config.ENVIRONMENT == 'DEV':
        logistics_wizard.debug = True

    # Register the blueprints for each version
    logistics_wizard.register_blueprint(demos_v1_blueprint, url_prefix='/api/v1')

    logistics_wizard.before_request(setup_auth_from_request)

    def exception_handler(e):
        """
        Handle any exception thrown in the interface layer and return
        a JSON response with the error details. Wraps python exceptions
        with a generic exception message.

        :param e:  The raised exception.
        :return:   A Flask response object.
        """
        if not isinstance(e, APIException):
            exc = APIException(u'Server Error',
                               internal_details=unicode(e))
        else:
            exc = e
        current_app.logger.error(exc)
        return Response(json.dumps(compose_error(exc, e)),
                        status=exc.status_code,
                        mimetype='application/json')

    def not_found_handler(e):
        current_app.logger.exception(e)
        if request_wants_json():
            status_code = 404
            return Response(json.dumps({
                                'code': status_code,
                                'message': 'Resource not found.'
                            }),
                            status=status_code,
                            mimetype='application/json')
        else:
            # TODO: Default to the root web page
            # return index()
            pass

    def bad_request_handler(e):
        current_app.logger.exception(e)
        status_code = 400
        return Response(json.dumps({
                            'code': status_code,
                            'message': 'Bad request.'
                        }),
                        status=status_code,
                        mimetype='application/json')

    # Register error handlers
    logistics_wizard.errorhandler(Exception)(exception_handler)
    logistics_wizard.errorhandler(400)(bad_request_handler)
    logistics_wizard.errorhandler(404)(not_found_handler)

    return logistics_wizard
