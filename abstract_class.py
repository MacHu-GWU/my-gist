#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
关于 ``abc`` 模块, 只要在母类中定义了抽象方法和属性，如果子类没有复写母类中所有的抽象方法
和属性，那么 **子类在实例化的过程中会抛出 TypeError**。


关于Python2/3的兼容，还请特别注意::

    @six.add_metaclass(abc.ABCMeta)
    class MyClassABC(object):
        @abc.abstractstaticmethod
        def staticmethod(): pass

或是::

    @six.add_metaclass(abc.ABCMeta)
    class MyClassABC(abc.ABCMeta):
        @staticmethod
        @abc.abstractmethod
        def staticmethod(): pass

并不能在子类实现 ``staticmethod`` 时，如果不是静态方法而是类方法或普通方法时抛出异常。

并且在Python2中不允许 ``@staticmethod`` 和 ``@abc.abstractmethod`` 叠加。
所以建议就安安静静的为所有的 ``regular method``, ``staticmethod``, ``classmethod``
加上 ``@abc.abstractmethod`` 而为所有的属性加上 ``@abc.abstractproperty`` 就好了。

正确的做法是::

    @six.add_metaclass(abc.ABCMeta)
    class MyClassABC(object):
        @abc.abstractmethod
        def method(self): raise NotImplementError

        @abc.abstractmethod
        def staticmethod(): raise NotImplementError

        @abc.abstractmethod
        def classmethod(cls): raise NotImplementError

        @abc.abstractproperty
        def property(self): raise NotImplementError

        @abc.abstractproperty
        def property_method(self): raise NotImplementError
"""

import abc
import six
import pytest


# --- Regular Method ---
@six.add_metaclass(abc.ABCMeta)
class BaseAbstractMethod(object):
    @abc.abstractmethod
    def method(self):
        raise NotImplementedError


class MyClassWrong(BaseAbstractMethod): pass


with pytest.raises(TypeError):
    myclass = MyClassWrong()


class MyClassRight(BaseAbstractMethod):
    def method(self): pass


myclass = MyClassRight


# --- Static Method ---
@six.add_metaclass(abc.ABCMeta)
class BaseAbstractStaticMethod(object):
    @staticmethod
    @abc.abstractstaticmethod
    def staticmethod():
        raise NotImplementedError


class MyClassWrong(BaseAbstractStaticMethod): pass


with pytest.raises(TypeError):
    myclass = MyClassWrong()


class MyClassRight(BaseAbstractStaticMethod):
    @staticmethod
    def staticmethod(): pass


myclass = MyClassRight()


# --- Property Method ---
@six.add_metaclass(abc.ABCMeta)
class BaseAbstractPropertyMethod(object):
    @property
    @abc.abstractmethod
    def property_method(self):
        raise NotImplementedError


class MyClassWrong(BaseAbstractPropertyMethod): pass


with pytest.raises(TypeError):
    my_class = MyClassWrong()


class MyClassRight(BaseAbstractPropertyMethod):
    @property
    def property_method(self): pass


myclass = MyClassRight()
