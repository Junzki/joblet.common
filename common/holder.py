# -*- coding:utf-8 -*-
import importlib
from typing import Dict, Optional
from common.utils.module_loading import import_string
from .conf import settings
from .components import LazyComponent
from .components.database import ComponentDatabase
from .exceptions import BadComponentKey, ComponentConflict, ComponentNotRegistered

BUILTIN_COMPONENTS = {
    'database': ComponentDatabase
}


class Holder(object):

    def __init__(self):
        self.settings = settings
        self.components: Dict[str, LazyComponent] = dict()

        for name in self.settings.REQUIRED_COMPONENTS:
            if name in BUILTIN_COMPONENTS:
                klass = BUILTIN_COMPONENTS[name]
                self.register_component(klass)
                continue

            try:
                mod = importlib.import_module(name)
            except ImportError:
                klass = import_string(name)
                self.register_component(klass)
                continue

            for obj_name in dir(mod):
                if obj_name.startswith('_'):
                    continue

                obj = getattr(mod, obj_name)
                if type(obj) is type and issubclass(obj, LazyComponent):
                    self.register_component(obj)
                elif isinstance(obj, LazyComponent):
                    self.register_component(type(obj))

    @staticmethod
    def get_component_key(k: str) -> str:
        t = k.lower().replace('-', '_').strip()
        if not t:
            raise BadComponentKey('component key should not be empty')

        return t

    def register_component(self, c, key: Optional[str] = None):
        assert issubclass(c, LazyComponent) or isinstance(c, LazyComponent), \
            "component must be a subclass of LazyComponent"

        if issubclass(c, LazyComponent):
            c = c()

        key = key or c.NAME
        k = self.get_component_key(key)
        if k in self.components:
            raise ComponentConflict('component %s already registered' % key)

        self.components[k] = c

        return self

    def get_component(self, key: str) -> LazyComponent:
        k = self.get_component_key(key)
        found = self.components.get(k)
        if not found:
            raise ComponentNotRegistered("required component %s not registered" % key)

        if not found.configured:
            found.explicit_setup()

        return found

    def __getattr__(self, item: str):
        return self.get_component(item)

    def __getitem__(self, item):
        return self.get_component(item)


holder = Holder()
