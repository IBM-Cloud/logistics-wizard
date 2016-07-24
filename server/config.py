from os import environ as env


class Config(object):

    ENVIRONMENT = env.get('LOGISTICS_WIZARD_ENV', 'DEV').upper()
    SD_STATUS = env.get('SD_STATUS', 'OFF')
    SECRET = env.get('SECRET', 'secret')
