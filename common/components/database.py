# -*- coding:utf-8 -*-
import os
from typing import Dict, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.ext.automap import automap_base
from common.conf import settings
from .base import LazyComponent

DEFAULT_DATABASE = 'default'
DEFAULT_SQLALCHEMY_POOL_SIZE = 5
DEFAULT_SQLALCHEMY_POOL_MAX_OVERFLOW = 10


class Database(object):
    Base = declarative_base()
    _url: str
    options: Dict[str, Any]

    def __init__(self, name: str = 'default'):
        conf = settings.DATABASES[name]
        schema = conf.pop('TYPE', 'postgresql').lower()

        self.options = dict()
        if schema.startswith('sqlite'):
            self._url = '{schema}:///{DBNAME}'.format(schema=schema, **conf)
        else:
            self._url = '{schema}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'.format(schema=schema, **conf)
            self.options.update(dict(
                pool_size=settings.SQLALCHEMY_POOL_SIZE or DEFAULT_SQLALCHEMY_POOL_SIZE,
                max_overflow=settings.SQLALCHEMY_POOL_MAX_OVERFLOW or DEFAULT_SQLALCHEMY_POOL_MAX_OVERFLOW,
                pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
            ))

        self.engine = None

    @property
    def url(self) -> str:
        return self._url

    def get_session(self) -> Session:
        if not self.engine:
            self.create_engine()

        return Session(self.engine)

    def create_engine(self):
        self.engine = create_engine(self._url, **self.options)

        enable_auto_map = settings.POSTGRES_AUTO_MAP
        if enable_auto_map:
            self.Base = automap_base()
            self.Base.prepare(self.engine, reflect=True)

        return self.engine

    @property
    def session(self) -> Session:
        return self.get_session()


class DatabaseProxy(object):
    default: str = DEFAULT_DATABASE

    def __init__(self, default: str = DEFAULT_DATABASE):
        self.default = default
        self.holder: Dict[str, Database] = dict()

    def register(self, name):
        db = Database(name)
        self.holder[name] = db

    def get(self, name: Optional[str] = None) -> Database:
        if not name:
            name = self.default

        return self.holder[name]

    def __getattr__(self, item):
        if item in self.holder:
            return self.get(item)

        conn = self.get()
        return getattr(conn, item)


class ComponentDatabase(LazyComponent):
    NAME = 'db'

    def _setup(self):
        default = getattr(settings, 'DEFAULT_DATABASE', DEFAULT_DATABASE)
        configure_alembic = getattr(settings, 'CONFIGURE_ALEMBIC', False)

        proxy = DatabaseProxy(default=default)
        conf = settings.DATABASES
        for name in conf.keys():
            proxy.register(name)

        if configure_alembic:
            url_ = proxy.get().url
            os.environ.setdefault('DATABASE_URL', url_)

        self._wrapped = proxy
