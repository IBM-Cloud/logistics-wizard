import os


class Config(object):

    ENVIRONMENT = os.environ.get('LOGISTICS_WIZARD_ENV', 'DEV').upper()
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/logistics_wizard')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

    SECRET = os.environ.get('SECRET', 'secret')