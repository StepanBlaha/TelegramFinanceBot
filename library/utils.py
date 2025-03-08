from binance.client import Client
import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

def get_dataframe(data):
    """
    Function for getting dataframe from given data
    :param data:
    :return: dataFrame
    """
    dataFrame = np.DataFrame(data)
    return dataFrame

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
    return datetime.fromtimestamp(unixTime/ 1000).strftime('%Y-%d-%m %H:%M:%S')