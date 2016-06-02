"""
Main app script to load a logistics wizard app model and either run it (DEV mode)
or make it available to the parent service as a WSGI module.

Configuration is done via environment variables. The current config keys
are:

DATABASE_URL     The url to connect to the database, defaults to a sqlite
                 file called 'test.db' in this module's directory.

         ENV     Set the environment flag, can be DEV, TEST, or PROD.
                 Defaults to DEV.

TOKEN_SECRET     The secret to be used for creating JSON Web Tokens, should
                 be long and hard to guess, like a password.

"""
import os
from flask_failsafe import failsafe
from werkzeug.serving import run_simple


# importable wsgi application
application = None


@failsafe
def create_app():
    """
    Wires the flask applications together into one wsgi app
    :return: A flask/wsgi app that is composed of multiple sub apps
    """
    from server import create_app
    return create_app()


def start_app():
    """
    Run in development mode, never used in production.
    """
    port = int(os.getenv("PORT", 5000))
    app = create_app()
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    start_app()
else:
    application = create_app()