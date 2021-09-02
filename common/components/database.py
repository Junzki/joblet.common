# -*- coding:utf-8 -*-
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.ext.automap import automap_base
from common.conf import settings
from .base import LazyComponent


class Database(object):
    Base = declarative_base()

    def __init__(self, name: str = 'default'):
        conf = settings.POSTGRES[name]
        url = 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'.format(**conf)

        pool_size = settings.SQLALCHEMY_POOL_SIZE or 5
        max_overflow = settings.SQLALCHEMY_POOL_MAX_OVERFLOW or 10
        pool_pre_ping = settings.SQLALCHEMY_POOL_PRE_PING

        self.engine = create_engine(url,
                                    pool_size=pool_size,
                                    max_overflow=max_overflow,
                                    pool_pre_ping=pool_pre_ping)

        enable_auto_map = settings.POSTGRES_AUTO_MAP
        if enable_auto_map:
            self.Base = automap_base()
            self.Base.prepare(self.engine, reflect=True)

    def get_session(self) -> Session:
        return Session(self.engine)

    @property
    def session(self) -> Session:
        return self.get_session()


class DatabaseProxy(object):

    def __init__(self):
        self.holder: Dict[str, Database] = dict()

    def register(self, name):
        db = Database(name)
        self.holder[name] = db

    def get(self, name: str = 'default') -> Database:
        return self.holder[name]

    def __getattr__(self, item):
        if item in self.holder:
            return self.get(item)

        conn = self.get()
        return getattr(conn, item)


class ComponentDatabase(LazyComponent):
    NAME = 'db'

    def _setup(self):
        proxy = DatabaseProxy()
        conf = settings.POSTGRES
        for name in conf.keys():
            proxy.register(name)

        self._wrapped = proxy
