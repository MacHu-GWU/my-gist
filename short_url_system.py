#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- 知乎, 短 URL 系统是怎么设计的？: https://www.zhihu.com/question/29270034
- 短网址服务系统如何设计: http://www.jianshu.com/p/d1cb7a51e7e5
- YouUrls, 一个PHP的实现: https://yourls.org/
- short_url for python: http://pypi.python.org/pypi/short_url
"""

from __future__ import print_function
import re
import time
import random
import string
import itertools

try:  # for Python2
    range = xrange
except:
    pass


def decimal_to_other_system(n, k):
    """Convert integer in decimal system into other system.

    Example: 6 = 110 in binary.

    decimal_to_other_system(6, 2) -> [0, 1, 1], +1

    Example: 20 = 14 in hex

    decimal_to_other_system(20, 16) -> [4, 1], +1

    :param n: integer
    :param k: k = 2 -> binary system, k = 16 -> hex system
    """
    l = list()
    while 1:
        d, m = divmod(n, k)
        l.append(m)
        if d == 0:
            break
        else:
            n = d
    return l


def test_decimal_to_other_system():
    l = decimal_to_other_system(6, 2)
    assert l == [0, 1, 1]

    l = decimal_to_other_system(20, 16)
    assert l == [4, 1]

test_decimal_to_other_system()


def int_to_surfix(i, charset, length):
    """Find the shorten url surfix by it's series number 

    Example: int_to_surfix(3, [A-Za-Z0-9], 6) = "caaaaa"

    :param i: the series number.
    :param charset: character set
    :paran length: how many char used as surfix    
    """
    l = decimal_to_other_system(i, len(charset))
    l.extend([0, ] * (length - len(l)))
    surfix = "".join([charset[n] for n in l])
    return surfix


def test_int_to_surfix():
    charset = string.ascii_lowercase
    assert int_to_surfix(0, charset, 6) == "aaaaaa"
    assert int_to_surfix(3, charset, 6) == "daaaaa"

test_int_to_surfix()


def permutation_url_surfix(charset, url_length):
    """Yield all possible url surfix.

    :param charset:
    :param url_length:

    When charset and url_length is large, it's very slow!
    """
    d = {i: char for i, char in enumerate(charset)}
    charset_len = len(charset)
    for i in range(charset_len ** url_length):
        l = decimal_to_other_system(i, charset_len)
        l.extend([0, ] * (url_length - len(l)))
        yield "".join([d[ind] for ind in l])


class BaseShortUrlService(object):

    """A short url service class. It support ``len(charset) ** url_length`` 
    different short url.

    1. 如果一个Url曾经出现过, 那么直接使用旧的surfix。
    2. 如果一个Url没有出现过, 那么给他发一个新surfix。
    """
    domain = None  # string, example "https://goo.gl/", has to endswith "/"
    charset = None  # string
    url_length = None  # integer
    ttl = 30 * 3600 * 24  # time to live

    def __init__(self):
        surfix_permutation = list(
            permutation_url_surfix(self.charset, self.url_length))
        random.shuffle(surfix_permutation)
        self.surfix_cycle = itertools.cycle(surfix_permutation)
        self.mapper = dict()

        pattern = "%s[%s]{%s}" % (self.domain, self.charset, self.url_length)
        self.valid_pattern = re.compile(pattern)

    @property
    def capacity(self):
        return len(self.charset) ** self.url_length

    def get(self, url):
        """Get a shortened url.
        """
        if url.startswith(self.domain):
            return url
        elif url in self.mapper:
            surfix = self.mapper[url]
        else:
            surfix = next(self.surfix_cycle)
            self.mapper[surfix] = url
            self.mapper[url] = surfix
        short_url = self.domain + surfix
        return short_url

    def parse(self, short_url):
        """Find the original url.
        """
        if re.match(self.valid_pattern, short_url) is not None:
            surfix = short_url.replace(self.domain, "")
            if surfix in self.mapper:
                return self.mapper[surfix]
            else:
                raise ValueError("There's no match.")
        else:
            raise ValueError("It's not a valid short url.")


if __name__ == "__main__":
    from sfm import rnd

    class GoogleShortUrlService(BaseShortUrlService):
        domain = "https://goo.gl/"
        charset = "abcdef0123456789"
        url_length = 3

    service = GoogleShortUrlService()
    print("This short url service can support %s urls" % service.capacity)

    # Generate some long url to shorten
    used_url = [rnd.simple_faker.fake.url() for i in range(1000)]
    for url in used_url:
        short_url = service.get(url)
        
    # Generate some test short url
    test_url = list()
    for i in range(20):
        short_url = "%s%s" % (
            service.domain,
            rnd.rand_str(service.url_length, service.charset),
        )
        test_url.append(short_url)

    for short_url in test_url:
        try:
            url = service.parse(short_url)
            print("%s -> %s" % (short_url, url))
        except Exception as e:
            print("No match for: %s" % short_url)
