import os


class Config(object):

    ENVIRONMENT = os.environ.get('LOGISTICS_WIZARD_ENV', 'DEV').upper()
    ERP = os.environ.get('ERP_SERVICE', 'http://logistics-wizard-erp.mybluemix.net/')
    SECRET = os.environ.get('SECRET', 'secret')
