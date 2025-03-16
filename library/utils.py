from binance.client import Client
import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
import time
from datetime import datetime
from mongoFunctions import *


def get_dataframe(data):
    """
    Function for getting dataframe from given data
    :param data:
    :return: dataFrame
    """
    dataFrame = np.DataFrame(data)
    return dataFrame





#Time conversion functions
def unix_to_date(unix, day = False):
    """
    Function that converts unix timestamp to datetime object
    :param unix: Unix timestamp
    :param day: Marker whether to return timestamp containing hours and minutes or not
    :return: datetime object
    """
    unixTime = int(unix)
    if day:
        return datetime.fromtimestamp(unixTime / 1000).strftime('%Y-%d-%m')
    return datetime.fromtimestamp(unixTime/ 1000).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_unix(datetime):
    """
    Function that converts datetime to unix timestamp
    :param datetime: Datetime to convert
    :return: Unix timestamp
    """
    return int(datetime.timestamp())

def seconds_to_unix(seconds):
    """
    Function that adds seconds to unix timestamp
    :param seconds: Seconds to convert
    :return: Unix timestamp
    """
    return int(time.time()) + seconds

def unix_to_timestamp(unix):
    """
    Function that converts unix timestamp to datetime object
    :param unix: Unix timestamp
    :return: Timestamp object
    """
    timestamp = datetime.fromtimestamp(unix)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def formatDatabaseResponse(col, userId=None, func=None):
    """
    Function that formats database's response into a message'
    :param col: Collection to select from
    :param userId: id of user to select
    :param func: function to select
    :return: formated database response
    """
    if func and userId:
        response = select(col, userId=userId, func=func)
        formatedResponse = "Here are your set functions:\n\n"
        for row in response:
            #Format  the response based on db
            if col == "Digest":
                # Format the interval
                if row["interval"]>86400:
                    interval = str((row["interval"]/86400)) + " Days"
                else:
                    interval = str((row["interval"]/3600)) + " Hours"
                # Format the record into a string
                record = f'Function: {row["function"]}, Symbol: {row["arguments"][0]}, Interval: {interval}'
                # Add to response string
            elif col == "Pricemonitor":
                record = f'Function: {row["function"]}, Symbol: {row["symbol"]}, Monitor change margin: {row["margin"]}%'
            else:
                record = "Invalid database"
            formatedResponse = formatedResponse + record
            formatedResponse = formatedResponse + '\n'
        return formatedResponse
    return "Not enough data"



# Function that formats database delete query
def formatDeleteQuery( userId, func, symbol, val):
    """
    Function that formats database delete query
    :param userId: id of user
    :param func: function
    :param symbol: symbol
    :param val: value
    :return: formated query string
    """
    if func == "digest":
        val = int(val)*3600
        query = {
            "userId": userId,
            "function": func,
            "arguments.0": symbol,
            "interval": val
        }

    elif func == "priceMonitor":
        val = int(val)
        query = {
            "userId": userId,
            "function": func,
            "symbol": symbol,
            "margin": val
        }
    else:
        return "Invalid database"
    return query


def formatUpdateQuery( format, newPrice=None, lastProcess=None, nextProcess=None):
    formatDict={
        "digest":{ "$set": { "lastProcess": lastProcess, "nextProcess": nextProcess }},
        "priceMonitor": {"$set": {"lastPrice":newPrice}}
    }
    query = formatDict[format]
    return query

def formatInsertQuery(format, userId, func, lastProcess=None, nextProcess=None, interval=None, symbol=None, margin=None, lastPrice=None, args=None):
    formatDict={
        "digest":
            {
                "userId": userId,
                "function": func,
                "arguments": args,
                "interval": interval,
                "lastProcess": lastProcess,
                "nextProcess": nextProcess
            },
        "priceMonitor":
            {
                "userId": userId,
                "function": func,
                "symbol": symbol,
                "margin": margin,
                "lastPrice": lastPrice
            }

    }


    try:
        query = formatDict[format]
        return query
    except Exception as e:
        return "Invalid set of arguments"