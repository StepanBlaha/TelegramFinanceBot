from mongo import *


def insert(user, interval, func, args, lastProcess, nextProcess):
    """

    :param user: Telegram user id
    :param interval: interval in which to execute function e. 1 day, 1 week,...
    :param func: function to execute
    :param args: arguments to pass to function
    :param lastProcess: time of the last function process
    :param nextProcess: calculated time of the next process
    :return:
    """
    DB = db_connect()
    collection = DB[""]

    data = {
        "userId": user,
        "function": func,
        "arguments": args,
        "interval": interval,
        "lastProcess": lastProcess
    }

    insertedId = collection.insert_one(data).inserted_id

