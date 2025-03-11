from mongo import *


def insert(user, period, func, args):
    DB = db_connect()
    collection = DB[""]

    data = {
        "userId": user,
        "period": period,
        "function": func,
        "arguments": args
    }

    insertedId = collection.insert_one(data).inserted_id

