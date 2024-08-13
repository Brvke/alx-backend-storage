#!/usr/bin/env python3
""" a module for the list_all function """


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.
    """

    try:
        documents = list(mongo_collection.find())
        return documents
    except:
        return []

