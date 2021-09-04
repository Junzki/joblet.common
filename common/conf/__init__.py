# -*- coding:utf-8 -*-
import importlib
import os

from common.exceptions import ImproperlyConfigured
from common.utils.functional import LazyObject
from . import default_settings

ENVIRONMENT_VARIABLE = 'JOBLET_CONFIG'


class Settings(object):

    TUPLE_SETTINGS = (
        'REQUIRED_COMPONENTS',
    )

    def __init__(self, settings_module):
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        self.SETTINGS_MODULE = settings_module
        mod = importlib.import_module(self.SETTINGS_MODULE)

        for setting in dir(mod):
            if setting.isupper():
                val = getattr(mod, setting)
                setattr(self, setting, val)


class LazySettings(LazyObject):

    def _setup(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise ImproperlyConfigured("Settings are not configured.")

        self._wrapped = Settings(settings_module)


settings = LazySettings()
