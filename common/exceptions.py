# -*- coding:utf-8 -*-


class JobletException(Exception):
    ...


class BadComponentKey(JobletException, ValueError):
    ...


class ComponentNotRegistered(JobletException):
    ...


class ComponentConflict(JobletException):
    """ Raises when component with same name already registered.
    """
    ...


class ImproperlyConfigured(JobletException):
    ...
