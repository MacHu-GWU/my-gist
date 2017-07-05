#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
attrdict是一个很赞的库, 可以允许你用attribute的语法风格来访问, 赋值, 修改字典
中的key, value。而其他的特性保持不变。

valid names:

1. 字符数字下划线。
2. 不以下划线开头。
3. 不是字典默认的方法名, 例如 dict.get。

ref: https://pypi.python.org/pypi/attrdict
"""

import pytest
from attrdict import AttrMap, AttrDict


def test_mutable():
    """

    注意: AttrDict中的sequence type会自动转化为tuple, 即非mutable的形式。也就是
    对list中的对象无法修改。如果想要允许对list中的对象进行修改, 需要使用AttrMap,
    并指定 ``sequence_type = list``。
    """
    user_data = {
        "id": "EN-0001",
        "phone_numbers": [
            {"label": "home", "number": "111-222-3333"},
            {"label": "work", "number": "444-555-6666"},
            {"label": "mobile", "number": "777-888-9999"},
        ],
        "profile": {
            "SSN": "123-45-6789",
            "drivers_license": {
                "state": "DC",
                "license_number": "DC-1234-5678",
            }
        }
    }
    user = AttrMap(user_data, sequence_type=list)

    assert user.id == "EN-0001"
    assert user["id"] == "EN-0001"

    user.id = "EN-0002"
    assert user.id == "EN-0002"
    assert user["id"] == "EN-0002"

    # nested dict is also attrdict
    assert user.phone_numbers[0].number == "111-222-3333"
    assert user.phone_numbers[0]["number"] == "111-222-3333"

    user.phone_numbers[0].number = "111-111-1111"
    assert user.phone_numbers[0].number == "111-111-1111"
    assert user.phone_numbers[0]["number"] == "111-111-1111"


def test_invalid_name():
    user_data = {
        "_id": 1,
        "first name": "John",
        "last name": "David",
        "email": "john.david@gmail.com",
    }
    user = AttrMap(user_data, sequence_type=list)

    # 无法用 dict.attr 的风格访问
    with pytest.raises(Exception):
        user._id
    # 但仍可以用 dict[attr] 的风格访问
    assert user["_id"] == 1


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
