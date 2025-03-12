from binance.client import Client
import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
import time
from datetime import datetime


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