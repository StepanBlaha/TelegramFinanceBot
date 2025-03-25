from bson import ObjectId
from pymongo.synchronous.database import Database

from mongo import *


def insert(col, query):
    """
    Function for inserting data into mongo db
    :param col: collection to insert into
    :param query: data to insert
    :return:
    """
    DB = db_connect()
    collection = DB[col]
    insertedId = collection.insert_one(query).inserted_id
    print(f'Successfully inserted {insertedId}')

#insert("Digest",12323213,2133, "digest",("skibi","di"), lastProcess=2017-12-2,nextProcess=2021-1-1)

def select(col, query=None):
    """
    Function for selecting data from mongo db
    :param col: collection to select from
    :param query: query to select
    :return: data from mongo db
    """
    DB = db_connect()
    collection = DB[col]
    DatabaseResponse = []

    if query:
        DatabaseResponse = collection.find(query)
    else:
        for record in collection.find():
            DatabaseResponse.append(record)

    return DatabaseResponse
#print(select("Digest", userId= 8106126437, func = "digest"))


def update(col, postId, values):
    """
    Function for updating data into mongo db
    :param col: collection to update into
    :param postId: post id to update
    :param values: values to update
    :return: response
    """
    DB = db_connect()
    collection = DB[col]
    query = {"_id": ObjectId(postId)}
    collection.update_one(query, values)
    return "Successfully updated"

def delete(col, query):
    """
    Function for deleting data from mongo db
    :param col: collection to delete from
    :param query: query to delete
    :return: response
    """
    #Connect to db and delete
    DB = db_connect()
    collection = DB[col]
    result = collection.delete_one(query)
    if result.deleted_count>0:
        return "Successfully deleted"
    else:
        return "Failed"
