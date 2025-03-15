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