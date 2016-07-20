import os


class Config(object):

    ENVIRONMENT = os.environ.get('LOGISTICS_WIZARD_ENV', 'DEV').upper()
    ERP = os.environ.get('ERP_SERVICE', 'http://0.0.0.0:3000/api/v1/')
    SECRET = os.environ.get('SECRET', 'secret')

    # Get VCAP_SERVICES variables
    if os.environ.get('VCAP_SERVICES') is not None:
        from json import loads
        SD_URL = loads(os.environ.get('VCAP_SERVICES'))['service_discovery'][0]['credentials']['url']
        SD_AUTH = loads(os.environ.get('VCAP_SERVICES'))['service_discovery'][0]['credentials']['auth_token']
    else:
        SD_URL = os.environ.get('SD_URL')
        SD_AUTH = os.environ.get('SD_AUTH')
