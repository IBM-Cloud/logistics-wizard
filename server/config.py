import os


class Config(object):

    ENVIRONMENT = os.environ.get('LOGISTICS_WIZARD_ENV', 'DEV').upper()
    ERP = os.environ.get('ERP_SERVICE', 'http://0.0.0.0:3000/api/v1/')
    SECRET = os.environ.get('SECRET', 'secret')
