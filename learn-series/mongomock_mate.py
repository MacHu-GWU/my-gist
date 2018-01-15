#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mongomock_mate is a simple script adding a data persistent layer to allow to
use mongomock as fake MongoDB.
"""

from __future__ import unicode_literals
from collections import OrderedDict
from superjson import json


def dump_db(db, path, verbose=True):
    data = OrderedDict()
    data["name"] = db.name
    data["_collections"] = OrderedDict()

    for col_name, col in db._collections.items():
        if col_name != "system.indexes":
            data["_collections"][col_name] = OrderedDict()
            data["_collections"][col_name]["_documents"] = col._documents
            data["_collections"][col_name]["_uniques"] = col._documents

    json.safe_dump(data, path, ensure_ascii=False, verbose=verbose)


def load_db(db, path, verbose=True):
    data = json.load(path, verbose=verbose)
    if data["name"] != db.name:
        raise ValueError("Wrong database file!")

    for col_name, col_data in data["_collections"].items():
        col = db.get_collection(col_name)
        col._documents = col_data["_documents"]
        col._uniques = col_data["_uniques"]



if __name__ =="__main__":
    import mongomock
    from datetime import datetime

    def test():
        db = mongomock.MongoClient().db
        col_user = db.user
        col_item = db.item
        col_order = db.order

        col_user.insert([
            {"_id": 1, "name": "Alice", "token": "g50!FvEd2eED".encode("utf-8")},
            {"_id": 2, "name": "Bob", "token": "2hF*nOv4*2f%".encode("utf-8")},
            {"_id": 3, "name": "Cathy", "token": "hA3m*MmJ&1*y".encode("utf-8")},
        ])

        col_item.insert([
            {"_id": 1, "name": "Apple"},
            {"_id": 2, "name": "Banana"},
            {"_id": 3, "name": "Cherry"},
        ])

        col_order.insert([
            {"_id": 1, "user": 1, "items": [{"item": 1, "quantity": 1}], "create_at": datetime(2017, 1, 1)},
            {"_id": 2, "user": 2, "items": [{"item": 2, "quantity": 2}], "create_at": datetime(2017, 1, 2)},
            {"_id": 3, "user": 3, "items": [{"item": 3, "quantity": 3}], "create_at": datetime(2017, 1, 3)},
        ])

        path = "db.json"
        dump_db(db, path, verbose=False)

        db = mongomock.MongoClient().db
        load_db(db, path, verbose=False)

        print(list(db.user.find()))
        print(list(db.item.find()))
        print(list(db.order.find()))

    test()