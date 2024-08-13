#!/usr/bin/env python3
""" a module for the  insert_school function """


def insert_school(mongo_collection, **kwargs):
    """
        Args:
            monmongo_collection: a pymongo collection object
            kwargs: key-value pair different documents

        Returns:
            _id of newly created document
    """

    return mongo_collection.insert_one(kwargs).inserted_id
