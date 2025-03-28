import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import json
import math
import io
import pandas as np

from binance.client import Client
from IndicatorFunctions import Indicators
from AiFunctions import AI
from UtilsFunctions import Utils
from IndicatorFunctions import Indicators

class Dataframe:
    def __init__(self, Client, Utils, Indicators):
        self.client = Client()
        self.utils = Utils()
        self.indicators = Indicators()

    # Function for getting pandas dataframe of EMA
    def get_ema_dataframe(self, symbol, period):
        """
        Function for getting pandas dataframe of EMA
        :param symbol: Symbol to get the dataframe of
        :param period: Days for measuring
        :return: Dataframe
        """
        # Get the Ema data and corresponding timestamps
        emas, timestamps = self.indicators.get_ema(symbol=symbol, emaDays=period, timestamp=True)
        # Replace the timestamps with unix
        for i in range(len(timestamps)):
            timestamps[i] = self.utils.unix_to_date(int(timestamps[i]), day=True)
        # Turn the data into dataframe
        data = {
            "EMA": emas,
            "Timestamp": timestamps
        }
        dataFrame = self.get_dataframe(data)
        dataFrame = dataFrame.to_string(index=False)
        return dataFrame

    # Function for getting pandas dataframe of KDJ
    def get_kdj_dataframe(self, symbol, period, df=False):
        """
        Function for getting pandas dataframe of KDJ
        :param symbol: Symbol to get the dataframe of
        :param period: Days for measuring
        :return: Dataframe
        """
        Ks, Ds, Js, closeTimes = self.indicators.get_kdj(symbol, int(period))
        data = {
            "K": Ks,
            "D": Ds,
            "J": Js,
            "Timestamp": closeTimes
        }
        dataFrame = self.get_dataframe(data)
        if df:
            return dataFrame
        dataFrame = dataFrame.to_string(index=False)
        return dataFrame

    def get_dataframe(self, data):
        """
        Function for getting dataframe from given data
        :param data:
        :return: dataFrame
        """
        dataFrame = np.DataFrame(data)
        return dataFrame
