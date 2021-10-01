# -*- coding:utf-8 -*-

DEBUG: bool = False

DEFAULT_DATABASE = 'default'
DATABASES = {
    'default': {
        'TYPE': 'sqlite',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
        'DBNAME': 'db.sqlite3'
    }
}

# Enable SQLAlchemy's "automap".
POSTGRES_AUTO_MAP: bool = False

SQLALCHEMY_POOL_SIZE: int = 5
SQLALCHEMY_POOL_MAX_OVERFLOW: int = 10
SQLALCHEMY_POOL_PRE_PING: bool = True

# Alembic (setup alembic required environ DATABASE_URL)
CONFIGURE_ALEMBIC = False
