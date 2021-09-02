# -*- coding:utf-8 -*-


DEBUG: bool = False

POSTGRES = {
    'HOST': '',
    'PORT': '',
    'USER': '',
    'PASSWORD': '',
    'DBNAME': ''
}

# Enable SQLAlchemy's "automap".
POSTGRES_AUTO_MAP: bool = False

SQLALCHEMY_POOL_SIZE: int = 5
SQLALCHEMY_POOL_MAX_OVERFLOW: int = 10
SQLALCHEMY_POOL_PRE_PING: bool = True
