#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mongomock是一个非常好用的用于测试pymongo或mongoengine相关代码的库。可以在不安装
MongoDB的情况下模拟database, collection的行为。

- github: https://github.com/mongomock/mongomock
"""

import pymongo
import mongomock


# --- 一个使用mongomock进行测试的例子 ---
def increase_votes(col):
    col.update({}, {"$inc": {"votes": 1}}, multi=True)


def test_increase_votes():
    """
    """
    col = mongomock.MongoClient().db.collection

    data = [{"votes": 1}, {"votes": 2}]
    for doc in data:
        doc["_id"] = col.insert(doc)

    increase_votes(col)

    for doc in data:
        stored_doc = col.find_one({"_id": doc["_id"]})
        stored_doc["votes"] -= 1
        # by comparing all fields we make sure only votes changed
        assert stored_doc == doc


test_increase_votes()


# --- 实验mongomock对insert, exception的支持 ---
def grouper_list(l, n):
    """Evenly divide list into fixed-length piece, no filled value if chunk
    size smaller than fixed-length.

    Example::

        >>> list(grouper(range(10), n=3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    **中文文档**

    将一个列表按照尺寸n, 依次打包输出, 有多少输出多少, 并不强制填充包的大小到n。

    下列实现是按照性能从高到低进行排列的:

    - 方法1: 建立一个counter, 在向chunk中添加元素时, 同时将counter与n比较, 如果一致
      则yield。然后在最后将剩余的item视情况yield。
    - 方法2: 建立一个list, 每次添加一个元素, 并检查size。
    - 方法3: 调用grouper()函数, 然后对里面的None元素进行清理。
    """
    chunk = list()
    counter = 0
    for item in l:
        counter += 1
        chunk.append(item)
        if counter == n:
            yield chunk
            chunk = list()
            counter = 0
    if len(chunk) > 0:
        yield chunk


def smart_insert(col, data, minimal_size=5):
    """An optimized Insert strategy.

    **中文文档**

    在Insert中, 如果已经预知不会出现IntegrityError, 那么使用Bulk Insert的速度要
    远远快于逐条Insert。而如果无法预知, 那么我们采用如下策略:

    1. 尝试Bulk Insert, Bulk Insert由于在结束前不Commit, 所以速度很快。
    2. 如果失败了, 那么对数据的条数开平方根, 进行分包, 然后对每个包重复该逻辑。
    3. 若还是尝试失败, 则继续分包, 当分包的大小小于一定数量时, 则使用逐条插入。
      直到成功为止。

    该Insert策略在内存上需要额外的 sqrt(nbytes) 的开销, 跟原数据相比体积很小。
    但时间上是各种情况下平均最优的。
    """
    import math

    if isinstance(data, list):
        # 首先进行尝试bulk insert
        try:
            col.insert(data)
        # 失败了
        except pymongo.errors.DuplicateKeyError:
            # 分析数据量
            n = len(data)
            # 如果数据条数多于一定数量
            if n >= minimal_size ** 2:
                # 则进行分包
                n_chunk = math.floor(math.sqrt(n))
                for chunk in grouper_list(data, n_chunk):
                    smart_insert(col, chunk, minimal_size)
            # 否则则一条条地逐条插入
            else:
                for doc in data:
                    try:
                        col.insert(doc)
                    except pymongo.errors.DuplicateKeyError:
                        pass
    else:
        try:
            col.insert(data)
        except pymongo.errors.DuplicateKeyError:
            pass


def test_smart_insert():
    """测试mongomock是否支持insert操作, 以及在raise exception的时候的行为。

    结论: 支持良好。
    """
    import time
    import random

    col = mongomock.MongoClient().db.collection

    def insert_test_data():
        col.remove({})

        data = [{"_id": random.randint(1, 10000)} for i in range(20)]
        for doc in data:
            try:
                col.insert(doc)
            except:
                pass
        assert 15 <= col.find().count() <= 20

    data = [{"_id": i} for i in range(1, 1 + 10000)]

    # Smart Insert
    insert_test_data()

    st = time.clock()
    smart_insert(col, data)

    assert col.find().count() == 10000  # after smart insert, we got 10000 doc

    # Regular Insert
    insert_test_data()

    st = time.clock()
    for doc in data:
        try:
            col.insert(doc)
        except:
            pass

    # after regular insert, we got 10000 doc
    assert col.find().count() == 10000


test_smart_insert()


# --- 测试mongomock对aggregate操作的支持 ---


def test_group():
    """测试mongomock是否支持group操作。

    结论: 支持。
    """
    col = mongomock.MongoClient().db.collection

    complexity = 10
    data = list()
    for i in range(complexity):
        for j in range(complexity):
            for k in range(complexity):
                data.append({"a": i, "b": j, "c": k})
    col.insert(data)

    pipeline = [
        {
            "$group": {"_id": {"a": "$a", "b": "$b"}},
        },
    ]

    for doc in col.aggregate(pipeline):
        print(doc)
        # print(len(list(col.aggregate(pipeline))))
        # assert len(list(col.aggregate(pipeline))) == 0  # expect be 100


test_group()
