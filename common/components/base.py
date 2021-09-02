# -*- coding:utf-8 -*-
from common.utils.functional import LazyObject


class LazyComponent(LazyObject):
    NAME: str

    def _setup(self):
        raise NotImplementedError('subclasses of LazyComponent must provide a _setup() method')

    def explicit_setup(self):
        self._setup()

    def shutdown(self):
        ...
