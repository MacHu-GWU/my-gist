#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of using `attrs <http://www.attrs.org/>`_
"""

import attr
from collections import OrderedDict


@attr.s
class MyClass(object):
    b = attr.ib()
    a = attr.ib()
    c = attr.ib()


MyClass.__attrs_attrs__
"""
This is list of Attribute(name='b', default=NOTHING, validator=...)
"""

my_class = MyClass(**dict(a=1, b=2, c=3))

print(attr.asdict(my_class))
"""
convert to dict, order not preserved.
"""

print(attr.astuple(my_class))
"""
convert to value tuple, order same as the attributes been defined.
"""

od = OrderedDict([
    (_attr.name, getattr(my_class, _attr.name)) for _attr in
    MyClass.__attrs_attrs__
])
print(od)
"""
convert to OrderedDict, order is same as the attributes been defined.
"""
