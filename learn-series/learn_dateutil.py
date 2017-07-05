#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Learn manipulating date time in Python. Local time, UTC time, parse string.

- dateutil: https://pypi.python.org/pypi/python-dateutil
- pytz: https://pypi.python.org/pypi/pytz
"""

from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import (
    tzlocal,
    tzutc,
)


def get_now_utc_time():
    """

    **中文文档**

    获得本地机器上的当地时间所对应的UTC时间。例如美国纽约的时区是
    Eastern Time Zone, UTC -05:00。也就是比UTC时间早5个小时。
    如果我们在2000-01-01 12:00:00运行此函数, 我们所期待得到的时间是07:00:00。
    """
    dt = datetime.utcnow()
    return dt

get_now_utc_time()


def get_local_timezone_info():
    """

    **中文文档**

    获得本地机器的时区信息。
    """
    tz = tzlocal()
    return tz

get_local_timezone_info()


def remove_timezone_info():
    """

    **中文文档**

    当时间带时区信息时候, 我们如果移除了时区信息, 剩下来的就是当地时间。
    在我们用parse方法从字符串获得时间时, 如果有时区信息, 则会带上时区信息。而
    有时候我们只需要用到本地时间来做计算, 那么我们就可以移除时区信息, 剩下的
    自然就是本地时间。
    """
    dt = parse("2000-01-01 17:00:00-05:00")
    dt = dt.replace(tzinfo=None)  # datetime.replace(tzinfo=None)

remove_timezone_info()


def convert_timezone_awared_time_to_utc_time(have_tzinfo=False):
    """

    :param have_tzinfo: whether retain the time zone information.

    **中文文档**

    将一个带时区的时间转化成UTC时间。对于UTC时间而言, 有没有时间信息都无所谓了。
    """
    dt = datetime.now(tzlocal())  # timezone awared local time
    utc_dt = dt.astimezone(tzutc())  # convert to utc time
    if have_tzinfo is False:
        utc_dt = utc_dt.replace(tzinfo=None)
    return utc_dt

convert_timezone_awared_time_to_utc_time(have_tzinfo=False)


def convert_utc_time_to_local_time(have_tzinfo=False):
    """

    :param have_tzinfo: whether retain the time zone information.

    **中文文档**

    将一个UTC时间转化为当地时间(或带时区的时间)。
    """
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=tzutc())
    local_dt = dt.astimezone(tzlocal())
    if have_tzinfo is False:
        local_dt = local_dt.replace(tzinfo=None)
    return local_dt

convert_utc_time_to_local_time(have_tzinfo=False)
