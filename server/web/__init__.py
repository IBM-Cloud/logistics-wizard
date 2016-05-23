"""
Initializer for the API application. This will create a new Flask app and
register all interface versions (Blueprints), initialize the database and
register app level error handlers.
"""
import re
import json

from flask import Flask, current_app, Response


def create_app():
    """
    Create the api as it's own app so that it's easier to scale it out on it's
    own in the future.

    :return:         A flask object/wsgi callable.
    """
    from server.config import Config
    from server.data import init_db, remove_session, wire_models
    from server.exceptions import APIException
    from server.web.utils import request_wants_json
    from server.web.rest.users import users_v1_blueprint, setup_user_from_request

    wire_models()

    # Create the app
    logistics_wizard = Flask('logistics_wizard', static_folder=None)
    # CORS(logistics_wizard, origins=[re.compile('.*')], supports_credentials=True)
    if Config.ENVIRONMENT == 'DEV':
        logistics_wizard.debug = True

    # Initialize the database (recreate if dev or test environment)
    drop = True if Config.ENVIRONMENT == 'TEST' else False
    init_db(drop)
    logistics_wizard.teardown_appcontext(remove_session)

    # Register the blueprints for each version
    logistics_wizard.register_blueprint(users_v1_blueprint, url_prefix='/api/v1')

    logistics_wizard.before_request(setup_user_from_request)

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
        return Response(json.dumps({'error': e.message}),
                        status=exc.status_code,
                        mimetype='application/json')

    def not_found_handler(e):
        current_app.logger.exception(e)
        if request_wants_json():
            return Response(json.dumps({'error': 'Resource not found.'}),
                            status=404,
                            mimetype='application/json')
        else:
            # TODO: Default to the root web page
            # return index()
            pass

    def bad_request_handler(e):
        current_app.logger.exception(e)
        return Response(json.dumps({'error': 'Bad request.'}),
                        status=400,
                        mimetype='application/json')

    # Register error handlers
    logistics_wizard.errorhandler(Exception)(exception_handler)
    logistics_wizard.errorhandler(400)(bad_request_handler)
    logistics_wizard.errorhandler(404)(not_found_handler)

    return logistics_wizard
