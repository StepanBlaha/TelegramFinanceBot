from bson import ObjectId
from pymongo.synchronous.database import Database

from mongo import *


def insertDigest(col, user, interval, func, args, lastProcess, nextProcess):
    """

    :param col: collection to insert into
    :param user: Telegram user id
    :param interval: interval in which to execute function e. 1 day, 1 week,...
    :param func: function to execute
    :param args: arguments to pass to function
    :param lastProcess: time of the last function process
    :param nextProcess: calculated time of the next process
    :return:
    """
    DB = db_connect()
    collection = DB[col]

    data = {
        "userId": user,
        "function": func,
        "arguments": args,
        "interval": interval,
        "lastProcess": lastProcess,
        "nextProcess": nextProcess
    }

    insertedId = collection.insert_one(data).inserted_id
    print(insertedId)

def insertPriceMonitor(col, user, margin, func, symbol, lastPrice):

    DB = db_connect()
    collection = DB[col]

    data = {
        "userId": user,
        "function": func,
        "symbol": symbol,
        "margin": margin,
        "lastPrice":lastPrice
    }

    insertedId = collection.insert_one(data).inserted_id
    print(insertedId)

#insert("Digest",12323213,2133, "digest",("skibi","di"), lastProcess=2017-12-2,nextProcess=2021-1-1)

def select(col, postId = None, time = None, userId = None, func = None):
    DB = db_connect()
    collection = DB[col]
    DatabaseResponse = []

    #If the post id is set select only set post
    if postId:
        query = { "_id": ObjectId(postId) }
        DatabaseResponse = collection.find(query)
        return DatabaseResponse

    # If time is sset select only the corresponding ones
    if time:
        query = { "nextProcess": time }
        DatabaseResponse = collection.find(query)
        return DatabaseResponse

    # Used for checking users set automatic functions
    if userId and func:
        print(func)
        query = { "userId": userId, "function": func }
        DatabaseResponse = collection.find(query)
        return DatabaseResponse

    for record in collection.find():
        DatabaseResponse.append(record)
    return DatabaseResponse

#print(select("Digest", userId= 8106126437, func = "digest"))


def update(col, postId, values):
    DB = db_connect()
    collection = DB[col]
    query = {"_id": ObjectId(postId)}
    collection.update_one(query, values)
    print("Successfully updated")

def delete(col, query):
    #Connect to db and delete
    DB = db_connect()
    collection = DB[col]
    result = collection.delete_one(query)
    if result.deleted_count>0:
        return "Successfully deleted"
    else:
        return "Failed"
