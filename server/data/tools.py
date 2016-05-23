"""
Database tools

Use the @db_script decorator to register a function as a database
init script. All db_scripts will be run automatically when the app
starts up (as long as they haven't already been run).
"""
from sqlalchemy import Column, String

from server.config import Config
from server.data import BaseModel


class _DBScript(BaseModel):
    """
    Model to track database scripts used to initialize data.
    """
    __tablename__ = 'db_script'

    name = Column(String(120), primary_key=True)


_scripts = []


def db_script(envs=None):
    """
    Decorator used to declare a function as a database setup script.
    Scripts will be tracked in the database so they only run once.

    :param envs:   An array of environments that this script applies to or "ALL"
    :return:       A wrapper function that returns a function that wil
                   raise an exception is called to avoid misuse..
    """
    if envs != 'ALL' and not isinstance(envs, list):
        raise ValueError('Must provide env list or \'ALL\'.')

    def decorated_function(func, *args, **kwargs):
        if envs != 'ALL':
            func.envs = [x.upper() for x in envs]
        else:
            func.envs = envs
        _scripts.append(func)
        return _do_not_run

    return decorated_function


def run_scripts():
    """
    Iterates through the registered setup scripts and runs any that have
    not already been run on this database.
    """
    # Load all of the scripts from the database since
    # we have to query each one anyway. The call to .get()
    # will user the cached object instead of querying again.
    _DBScript.query.all()
    for script in _scripts:
        if _should_run_script(script):
            script()
            _DBScript(name=script.__name__).save()


def _should_run_script(script):
    """
    Check if this script should run here. First check that it's supposed
    to run for this environment, then check if it's already been run.

    :param script:   The script to check. Must have .env property set to
                     either 'ALL' or an array of acceptable environments.
    :return:         True is the script should be run.
    """
    if script.envs == 'ALL' or Config.ENVIRONMENT in script.envs:
        return _DBScript.query.get(script.__name__) is None
    else:
        return False


def _do_not_run():
    """
    Raise an exception because this function should never run.
    """
    raise Exception('Do not run db_scripts directly.')
