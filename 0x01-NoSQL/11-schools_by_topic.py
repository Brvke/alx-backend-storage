#!/usr/bin/env python3
""" a module housing the schools_by_topic function """


def schools_by_topic(mongo_collection, topic):
    """ 
        Arsgs:
            mongo_collection: a pymongo collection object
            topic: a search string
        Return:
            a cursor object of a school with the following topic
    """
    return mongo_collection.find({"topics" : {"$in": [topic]}})
