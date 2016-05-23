"""
The Database layer.

Uses a thread-local (scoped) db session that is exposed as a global
for importing from the service layer.

Checks the following environment variables for the SQL connection string:
    DATABASE_URL
    SQLALCHEMY_DATABASE_URI

Public properties:

Base       - Parent class that Models should inherit from. Includes a query
             property so that querying can be done via Model.query.filter(...)

db         - The scoped session object. Each thread get's it's own view of this
             property. When the thread is finished (request context is going
             away) you must call db.remove().
"""
from threading import local
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from server.config import Config
from server.data.utils import parse_search_fields, build_text_filter

tl_local = local()
_engine = create_engine(Config.DATABASE_URL, convert_unicode=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
_db = scoped_session(Session)
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise AttributeError('\'{}\' object has no attribute \'{}\''.format(type(self).__name__, key))

    query = _db.query_property()

    @classmethod
    def search(cls, search_string):
        fields = parse_search_fields(search_string)
        filters = build_text_filter(cls, fields)
        return cls.query.filter(*filters)

    @classmethod
    @contextmanager
    def transaction(cls):
        tl_local.transaction = True
        try:
            yield
            _db.commit()
        except:
            _db.rollback()
            raise
        finally:
            tl_local.transaction = False

    @property
    def session(self):
        if getattr(tl_local, 'transaction', None):
            return _db
        else:
            return self.query.session

    def delete(self):
        self.session.delete(self)
        # Only commit if we are not in a transaction
        if not getattr(tl_local, 'transaction', None):
            self.session.commit()

    def save(self):
        self.session.add(self)
        # Only commit if we are not in a transaction
        if not getattr(tl_local, 'transaction', None):
            self.session.commit()


def init_db(drop=False):
    """
    Initialize the database. Must be explicitly called during app setup
    so that there is no race condition on initializing the db from multiple
    request contexts.

    :param drop:  True to drop all tables in the database and recreate them.
    """
    # Import modules that define models so that all metadata is setup
    # for table creation
    from server.data.tools import run_scripts

    if drop:
        BaseModel.metadata.drop_all(bind=_engine)
    BaseModel.metadata.create_all(bind=_engine)
    run_scripts()


def remove_session(*args, **kwargs):
    """
    Close the current session. Call when the thread (or request) is finishing
    and will no longer need to access the database.
    """
    _db.remove()


def wire_models():
    """
    Import all of the models so that SQLAlchemy has all of the necessary metadata setup
    """
    from server.data import users, db_scripts
