"""
Parent application that loads any child applications at their proper
paths. If we end up doing the static parts completely separately, this can
just load the API app directly.
"""
from server.exceptions import AuthenticationException


def create_app():
    """
    Wires the flask applications together into one wsgi app

    :return:        A flask/wsgi app that is composed of multiple sub apps
    """
    from server.web import create_app
    # If we do a static javascript app via flask, add it here
    # from server.web import create_app as create_web_app
    return create_app()
