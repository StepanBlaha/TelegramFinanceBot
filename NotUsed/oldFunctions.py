#Function for updating data in digest collection
def updateDigest(col, postId, lastProcess, nextProcess):
    DB = db_connect()
    collection = DB[col]

    query = { "_id": ObjectId(postId) }
    newValues = { "$set": { "lastProcess": lastProcess, "nextProcess": nextProcess }}
    collection.update_one(query, newValues)
    print("Successfully updated")

#Function for updating data in price monitor collection
def updatePriceMonitor(col, postId, newPrice):
    DB = db_connect()
    collection = DB[col]
    query = {"_id": ObjectId(postId)}
    newValues = {"$set": {"lastPrice":newPrice}}
    collection.update_one(query, newValues)
    print("Successfully updated")

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
        "lastPrice": lastPrice
    }

    insertedId = collection.insert_one(data).inserted_id
    print(insertedId)