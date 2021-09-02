# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.ext.automap import automap_base
from common.conf import settings
from .base import LazyComponent


class Database(object):
    Base = declarative_base()

    def __init__(self):
        conf = settings.POSTGRES
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


class ComponentDatabase(LazyComponent):
    NAME = 'db'

    def _setup(self):
        self._wrapped = Database()
