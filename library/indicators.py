from binance.client import Client
import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import json

from ai.chatgptFunctions import gptTradeAdvice
from library.utils import *
import io


from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)
from TelegramBotFunctions import *
client = Client()




# Function for getting atr of given symbol
def get_atr(symbol, period = 30, dictionary=False):
    """
    Function for getting atr of given symbol
    :param symbol: symbol to calculate atr of
    :param period: period of atr
    :param dictionary: if true returns dictionary with more data
    :return: final atr over the last period/30 days
    """
    InitialRTAPeriod = 14

    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, start_str=f"{period + 1} days ago")
    closingPrices = get_data_from_klines(klines, "Close price")
    highPrices = get_data_from_klines(klines, "High price")
    lowPrices = get_data_from_klines(klines, "Low price")

    InitialTRs = []
    TRs = []
    ATRs = []

    for i in range(1, len(closingPrices)):
        # Calculate TR
        TR = max(highPrices[i] - lowPrices[i], abs(highPrices[i] - closingPrices[i-1]), abs(lowPrices[i] - closingPrices[i-1]))
        if i < InitialRTAPeriod + 1:
            InitialTRs.append(TR)
        else:
            TRs.append(TR)
    # Calculate initial ATR
    BaseATR = sum(InitialTRs) / len(InitialTRs)
    ATR = BaseATR
    ATRs.append(ATR)

    # Calculate the rest of ATRs using wilders formula
    for i in range(len(TRs)):
        # Calculate the ATR using the smoothing formula
        ATR = ( ATR * (InitialRTAPeriod - 1) + TRs[i]) / InitialRTAPeriod
        ATRs.append(ATR)

    if dictionary:
        data = {
            "ATRs": ATRs,
            "TRs": InitialTRs + TRs,
            "BaseATR": BaseATR,
            "ATR": ATR
        }

        return data

    return ATR

#Function for getting 14 day rsi for symbol
def get_rsi(symbol):
    """
    Function for getting RSI of given symbol
    :param symbol: The symbol to get RSI
    :return: The RSI of the symbol
    """
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, start_str="15 days ago")
    closePrices = get_closing_prices(klines)
    gains = []
    loses = []
    differences = pd.diff(closePrices)
    for i in range(len(differences)):
        if differences[i] > 0:
            gains.append(differences[i])
            loses.append(0)
        elif differences[i] < 0:
            loses.append(abs(differences[i]))
            gains.append(0)

    averageGain = sum(gains) / 14
    averageLoss = sum(loses) / 14

    if averageLoss == 0:
        rsi = 100
    else:
        rs = averageGain / averageLoss
        rsi = 100 - (100/(1 + rs))

    return rsi

# Function for calculating SMA of given symbol in the range of given days
def get_sma(symbol, days):
    """
    Function for calculating SMA of given symbol in the range of given days
    :param symbol: The symbol for calculating the sma of
    :param days: The number of days for calculations
    :return: SMA of given symbol
    """
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, start_str=f"{days+1} days ago")
    closePrices = get_closing_prices(klines)
    sma = sum(closePrices) / len(closePrices)
    return sma

# Function for calculating EMA for given days
def get_ema(symbol, emaDays = 14, smaDays = 10, timestamp = False):
    """
    Function for calculating EMA for given days
    :param symbol: The symbol for calculating the ema of
    :param emaDays: The number of days for ema calculations
    :param smaDays: The number of days for calculating the starting SMA
    :param timestamp: Flag for checking if you want to also return corresponding timestamps
    :return: List of EMAs of given symbol over the span of given days
    """
    # Get the klines
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, start_str=f"{emaDays} days ago")
    # Extract the closing prices
    closePrices = get_closing_prices(klines)
    timestamps = get_data_from_klines(klines, "Close time")
    # Get SMA
    sma = get_sma(symbol, smaDays)
    alpha = 2 / (emaDays + 1)
    emas = []
    # Get the EMAs
    for i in range(len(closePrices)):
        currentPrice = closePrices[i]
        if len(emas) == 0 :
            ema = alpha * currentPrice + (1 - alpha) * sma
            emas.append(ema)
        else:
            lastEma = emas[-1]
            ema = alpha * currentPrice + (1 - alpha) * lastEma
            emas.append(ema)
    if timestamp:
        return emas, timestamps
    return emas

# Function for calculating KDJ for given symbol over the given period of time
def get_kdj(symbol, period):
    """
    Function for calculating KDJ for given symbol over the given period of time
    :param symbol: Symbol to calculate KDJ of
    :param period: Period of time for calculation
    :return:
    """
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, start_str=f"{period} days ago")
    closePrices = get_data_from_klines(klines, "Close price")
    highPrices = get_data_from_klines(klines, "High price")
    lowPrices = get_data_from_klines(klines, "Low price")
    closeTimes = get_data_from_klines(klines, "Close time")
    # Lists for the KDJs
    Ks = []
    Ds = []
    Js = []
    for i in range(period):
        # Lowest prices till the day
        low = lowPrices[:(i+1)]
        # Highest prices till the day
        high = highPrices[:(i+1)]
        close = closePrices[i]
        # Calculate the K
        K = (close - min(low)) / (max(high) - min(low)) * 100
        Ks.append(K)
        # If you have K data from more than 3 days calculate the other metrics
        if len(Ks) > 2 :
            # Get last three Ks
            lastThreeKs = Ks[-3:]
            # Calcutale the D
            D = sum(lastThreeKs) / len(lastThreeKs)
            Ds.append(D)
            #Calculate the J
            J = 3 * K - 2 * D
            Js.append(J)
        else:
            Ds.append(0)
            Js.append(0)
    for i in range(len(closeTimes)):
        closeTimes[i] = unix_to_date(int(closeTimes[i]), day = True)
    return Ks, Ds, Js, closeTimes

