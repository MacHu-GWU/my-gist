#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sqlitedict支持Multi Thread Safe Write。也就是可以用多线程或是多个脚本对同一个
字典进行写操作。
"""

from __future__ import print_function
import os
import time
import string
import random
from multiprocessing.dummy import Pool
from sqlitedict import SqliteDict


file = "./sqlitedict.sqlite"
mydict = SqliteDict(file, autocommit=True)
mydict.clear()


def multiple_script():
    """多个脚本调用同一个字典。
    """
    s = "x" * 10000
    
    st = time.clock()
    for i in range(10000):
        mydict[str(i)] = s
    elapsed = time.clock() - st
    print("elapsed %.6f seconds." % elapsed)
    assert len(mydict) == 10000
    
# multiple_script()


def multi_thread():
    """多个线程调用同一个字典。
    """
    s = "x" * 10000
    def assign(i):
        mydict[str(i)] = s
        
    st = time.clock()
    pool = Pool(8)
    pool.map(assign, range(10000))
    elapsed = time.clock() - st
    print("elapsed %.6f seconds." % elapsed)
    assert len(mydict) == 10000
    
# multi_thread()