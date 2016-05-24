import os


class Config(object):

    ENVIRONMENT = os.environ.get('LOGISTICS_WIZARD_ENV', 'DEV').upper()

    SECRET = os.environ.get('SECRET', 'secret')
