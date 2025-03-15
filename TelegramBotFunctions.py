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

client = Client()
# Get historical trades
# tr = client.get_historical_trades(symbol = "BTCUSDT", limit=10)
# print(tr)

# Function for getting specific data from given klines
def get_data_from_klines(klines, desiredData):
    """
    Function for getting specific data from given klines
    :param klines: List with kline data
    :param desiredData: Type of data
    :return: List of desired data
    """
    dataTypes = {
        "Open time": 0,
        "Open price": 1,
        "High price": 2,
        "Low price": 3,
        "Close price": 4,
        "Volume": 5,
        "Close time": 6,
        "Quote asset volume": 7,
        "Number of trades": 8,
        "Taker buy base asset volume": 9,
        "Taker buy quote asset volume": 10
    }
    dataList = []
    dataIndex = dataTypes[desiredData]
    for i in range(len(klines)):
        currentKline = klines[i]
        dataList.append(float(currentKline[dataIndex]))
    return dataList

# Function for calculating the average order values for given symbol
def get_average_order_values(symbol):
    """
    Function for calculating the average order values for given symbol
    :param symbol:
    :return : Average prices and quantities of bids and asks
    """
    orders = client.get_order_book(symbol=symbol, limit = 20)
    bids = orders['bids'] # buy orders
    asks = orders['asks'] # sell order
    # Calulate the averages
    averageSellQuantity = 0
    averageBuyQuantity = 0
    averageSellPrice = 0
    averageBuyPrice = 0
    for i in range(len(bids)):
        averageBuyPrice = averageBuyPrice + float(bids[i][0])
        averageBuyQuantity = averageBuyQuantity + float(bids[i][1])
    for i in range(len(asks)):
        averageSellPrice = averageSellPrice + float(asks[i][0])
        averageSellQuantity = averageSellQuantity + float(asks[i][1])

    averageSellQuantity = averageSellQuantity / len(asks)
    averageBuyQuantity = averageBuyQuantity / len(bids)
    averageSellPrice = averageSellPrice / len(asks)
    averageBuyPrice = averageBuyPrice / len(bids)

    response = f"Average offered price: {averageSellPrice}\n Average offered quantity: {averageSellQuantity}\n Average asked price: {averageBuyPrice}\n Average asked quantity: {averageBuyQuantity}"
    return response

# Function for getting info about recent trades of given symbol including the average price and quantity
def get_recent_trade_info(symbol, limit):
    """
    Function for getting info about recent trades of given symbol including the average price and quantity
    :param symbol:
    :return : Average, minimal and maximal prices and quantities of trades
    """
    trades = client.get_recent_trades(symbol = symbol, limit = limit)
    tradeQuantities = []
    tradePrices = []
    for i in range(len(trades)):
        tradeQuantities.append(float(trades[i]['qty']))
        tradePrices.append(float(trades[i]['price']))

    averageTradeQuantity = (sum(tradeQuantities) / len(tradeQuantities))
    averageTradeQuantity = f"{averageTradeQuantity:.8f}"
    averageTradePrice = (sum(tradePrices) / len(tradePrices))
    MaxTradePrice = max(tradePrices)
    MinTradePrice = min(tradePrices)
    MaxTradeQuantity = min(tradeQuantities)
    MaxTradeQuantity =f"{MaxTradeQuantity:.8f}"
    MinTradeQuantity = min(tradeQuantities)
    MinTradeQuantity = f"{MinTradeQuantity:.8f}"

    formatedString =f'Average trade quantity: {averageTradeQuantity}\n Average trade price: {averageTradePrice}\n Minimum trade price: {MinTradePrice}\n Maximum trade price: {MaxTradePrice}\n Minimun trade quantity: {MinTradeQuantity}\n Maximum trade quantity: {MaxTradeQuantity}\n'
    return formatedString

# Function for getting prices of given symbol over the last period days
def get_historical_prices(symbol, period):
    """
    Function for getting prices of given symbol over the last period days
    :param symbol: symbol to get prices of
    :param period: span of days to track
    :return: list of prices
    """
    klines = client.get_historical_klines(symbol = symbol, interval = client.KLINE_INTERVAL_1HOUR, start_str =f"{period} days ago")
    closingPrices = get_data_from_klines(klines,"Close price")
    return closingPrices

# Function for showing basic info about given symbol
def format_symbol_info(symbol_name, period = 14):
    """
    Function for showing basic info about given symbol
    :param symbol_name:
    :return: Info
    """
    #Gets all the exchange pairs
    exchange_info = client.get_exchange_info()
    trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols']]
    #Checks for invalid user pair
    if symbol_name not in trading_pairs:
        return "Invalid symbol name."
    #Returns the info about the symbol
    symbol = client.get_symbol_info(symbol=symbol_name)
    #Returns the last price of symbol
    last_price = client.get_symbol_ticker(symbol=symbol_name)
    #Get the market state of the symbol
    market_depth = get_average_order_values(symbol=symbol_name)
    #Get recent trades of symbol
    recent_trades = get_recent_trade_info(symbol=symbol_name, limit=10)
    #Get recent prices
    recent_prices = get_historical_prices(symbol['symbol'], period)

    tradeAdvice = gptTradeAdvice(symbol["symbol"], period, recent_prices, recent_trades, market_depth).capitalize()


    response = f"Symbol: {symbol['symbol']}\n Status: {symbol['status']}\n Price: {last_price['price']}\n Trade advice: {tradeAdvice}\n\n Current market: \n {market_depth}\n\n Recent trades: \n {recent_trades}\n "
    return response

# Function for getting the market pattern base on the opening and closing price
def get_price_trend( openingPrice, closingPrice):
    """
    Function for getting the market pattern base on the opening and closing price
    :param openingPrice: The opening price of current kline
    :param closingPrice: The closing price of current kline
    :return: Type of trend
    """
    acceptableMargin = openingPrice / 100
    if closingPrice - openingPrice > acceptableMargin:
        return "bullish"
    elif closingPrice - openingPrice < acceptableMargin:
        return "bearish"
    else:
        return "neutral"



def plot_kline_dataframe(symbol):
# NEFUNGUJE SPRAVNE PLOTTING
    #MUSIM PREPRACOVAT
    #SPRAVNE JE STRUKTURA list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

    klines = client.get_historical_klines(symbol = symbol, interval = client.KLINE_INTERVAL_1HOUR, start_str ="7 days ago" )
    openPrices = [] # Opening prices of klines
    closePrices = [] # Closing prices of klines
    highPrices = [] # Highest prices of klines
    lowPrices = [] # Lowest prices of klines
    timestamps = [] # Timestamps of klines
    numberOfTrades = [] # Number of trades made
    tradeVolumes = [] # Amount of actives traded

    averageTradeVolumes = [] # Calculated average trade volume for each kline
    marketPatterns = [] # List containing the market patterns of each kline

    for i in range(len(klines)):
        currentKline = klines[i]
        timestamps.append(float(currentKline[0]))

        openPrices.append(float(currentKline[1]))
        highPrices.append(float(currentKline[2]))
        lowPrices.append(float(currentKline[3]))
        closePrices.append(float(currentKline[4]))

        tradeVolumes.append(float(currentKline[5]))
        numberOfTrades.append(float(currentKline[8]))

        averageTradeVolumes.append(float(currentKline[5]) / float(currentKline[8]))
        currentPatern = get_price_trend(openingPrice = float(currentKline[1]), closingPrice = float(currentKline[4]))
        marketPatterns.append(currentPatern)

    dataSet = {
        "Time": timestamps,
        "Number of trades": numberOfTrades,
        "Trade volume": tradeVolumes,
        "Average volume per trade": averageTradeVolumes,
        "Highest price": highPrices,
        "Lowest price": lowPrices,
        "Opening price": openPrices,
        "Closing price": closePrices,
        "Market pattern": marketPatterns

    }
    dataFrame = np.DataFrame(dataSet)
    dataFrame.plot()
    plt.show()
    print(dataFrame)
#plot_kline_dataframe("BTCUSDT")

#Function for generating graph of prices of symbol over specified period
def plot_price_in_time(symbol, period):
    """
    Function for generating graph of prices of symbol over specified period
    :param symbol: Symbol to plot
    :param period: Number of days to plot
    :return:
    """
    klines = client.get_historical_klines(symbol = symbol, interval = client.KLINE_INTERVAL_1HOUR, start_str =f"{period} days ago")
    timestamps = []
    closingPrices = []
    for i in range(len(klines)):
        currentKline = klines[i]
        curTime = unix_to_date(int(currentKline[6]))
        timestamps.append(curTime)
        closingPrices.append(float(currentKline[4]))

    plt.plot(timestamps, closingPrices)
    # Calculate the timestamp stepsize
    num_ticks = 10
    step = len(timestamps) // num_ticks

    plt.xticks(timestamps[::step], rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3, left=0.15)
    plt.title(f"{symbol} Historical Prices")
    IoStream = io.BytesIO()
    plt.savefig(IoStream, format='png')
    IoStream.seek(0)
    plt.close('all')

    return IoStream

print(plot_price_in_time("BTCUSDT", 7))

# Function to extract closing prices from given kline list
def get_closing_prices(klines):
    """
    Function to extract closing prices from given kline list
    :param klines: List of kline data
    :return: List of closing prices
    """
    closingPrices = []
    for i in range(len(klines)):
        currentKline = klines[i]
        closingPrices.append(float(currentKline[4]))
    return closingPrices

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
#print(get_rsi("BTCUSDT"))

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

# Function for getting pandas dataframe of EMA
def get_ema_dataframe(symbol, period):
    """
    Function for getting pandas dataframe of EMA
    :param symbol: Symbol to get the dataframe of
    :param period: Days for measuring
    :return: Dataframe
    """
    # Get the Ema data and corresponding timestamps
    emas, timestamps = get_ema(symbol=symbol, emaDays=period, timestamp=True)
    # Replace the timestamps with unix
    for i in range(len(timestamps)):
        timestamps[i] = unix_to_date(int(timestamps[i]), day=True)
    # Turn the data into dataframe
    data = {
        "EMA": emas,
        "Timestamp": timestamps
    }
    dataFrame = get_dataframe(data)
    dataFrame = dataFrame.to_string(index=False)
    return dataFrame

# Function for getting graph of EMA for given symbol over period of time
def plot_ema(symbol, period):
    """
    Function for getting graph of EMA for given symbol over period of time
    :param symbol: Symbol to calculate EMA of
    :param period: Period of time for calculation
    :return: Ema graph of given symbol
    """
    # Get the Ema data and corresponding timestamps
    emas, timestamps = get_ema(symbol = symbol, emaDays = period, timestamp= True)
    # Replace the timestamps with unix
    for i in range(len(timestamps)):
        timestamps[i] = unix_to_date(int(timestamps[i]), day=True)
    # Plot setup
    plt.plot(timestamps, emas, marker='o')
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.3, left=0.15)
    plt.title(f"{symbol} EMA data")
    IoStream = io.BytesIO()
    plt.savefig(IoStream, format='png')
    IoStream.seek(0)
    plt.close('all')

    return IoStream

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

# Function for getting pandas dataframe of KDJ
def get_kdj_dataframe(symbol, period, df = False):
    """
    Function for getting pandas dataframe of KDJ
    :param symbol: Symbol to get the dataframe of
    :param period: Days for measuring
    :return: Dataframe
    """
    Ks, Ds, Js, closeTimes = get_kdj(symbol, int(period))
    data = {
        "K": Ks,
        "D": Ds,
        "J": Js,
        "Timestamp": closeTimes
    }
    dataFrame = get_dataframe(data)
    if df:
        return dataFrame
    dataFrame = dataFrame.to_string(index=False)
    return dataFrame
print(get_kdj_dataframe("BTCUSDT", 14))
# Function for getting graph of KDJ for given symbol over period of time
def plot_kdj(symbol, period):
    """
    Function for getting graph of KDJ for given symbol over period of time
    :param symbol: Symbol to calculate KDJ of
    :param period: Period of time for calculation
    :return:
    """
    Ks, Ds, Js, closeTimes = get_kdj(symbol, period)
    plt.plot(closeTimes, Ks, label="K")
    plt.plot(closeTimes, Ds, label="D")
    plt.plot(closeTimes, Js, label="J")
    # Plot setup
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.2)
    plt.title(f"{symbol} KDJ data")
    plt.legend()
    IoStream = io.BytesIO()
    plt.savefig(IoStream, format='png')
    IoStream.seek(0)
    plt.close('all')

    return IoStream

# Function for getting the current price of given symbol
def current_price(symbol):
    """
    Function for getting the current price of given symbol
    :param symbol: Symbol to calculate current price
    :return: Current price
    """
    symbolPrice = client.get_symbol_ticker(symbol=symbol)
    return symbolPrice["price"]

# Function for getting the recent traded volume of given symbol
def get_recent_traded_volume(symbol, period):
    """
    Function for getting the recent traded volume of given symbol
    :param symbol: Symbol to calculate recent traded volume
    :param period: Period of time for calculation
    :return: Traded volume
    """
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1HOUR, start_str=f"{period} days ago")
    volumes = get_data_from_klines(klines, "Volume")
    volume = sum(volumes)
    return volume

# Function for getting the number of recent trades of given symbol
def get_number_of_recent_trades(symbol, period):
    """
    Function for getting the number of recent trades of given symbol
    :param symbol: Symbol to calculate number of recent trades
    :param period: Period of time for calculation
    :return: Number of recent trades
    """
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1HOUR, start_str=f"{period} days ago")
    Trades = get_data_from_klines(klines, "Number of trades")
    tradeNumber = sum(Trades)
    return tradeNumber

# Function for getting the latest price trend
def get_recent_trend(symbol, period):
    """
    Function for getting the recent trend of given symbol
    :param symbol: Symbol to calculate recent trend
    :param period: Period of time for calculation
    :return: Trend
    """
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1HOUR, start_str=f"1 hour ago")
    openingPrice = get_data_from_klines(klines, "Open price")
    closingPrice = get_data_from_klines(klines, "Close price")
    trend = get_price_trend(float(openingPrice[0]), float(closingPrice[0]))
    return trend



def trade_advice(symbol, period):
    """
    Custom function for giving suggestions on whether o buy or sell
    :param symbol: symbol to calculate suggestions
    :param period: period of time for calculation
    :return: Buy/Sell suggestions
    """
    # Maybe pridam jeste buz oir sell podle recent trade
    buy = 0
    sell = 0
    # Get buy/sell based on rsi
    rsi = get_rsi(symbol)
    if rsi >70:
        sell+=1
    elif rsi<30:
        buy+=1

    # Get buy/sell based od kdj
    kdj = get_kdj_dataframe(symbol, period, df=True)
    signals = []

    for i in range(1, len(kdj)):
        if kdj["K"][i] > kdj["D"][i] and kdj["K"][i-1] <= kdj["D"][i-1] and kdj['J'][i] > 20 and kdj['J'][i-1] <= kdj['J'][i]:
            signals.append("buy")
        elif kdj['K'][i] < kdj['D'][i] and kdj['K'][i - 1] >= kdj['D'][i - 1] and kdj['J'][i] < 80 and kdj['J'][i - 1] >= kdj['J'][i]:
            signals.append("sell")
    if signals[len(signals)-1] == "buy":
        buy+=1
    else:
        sell+=1

    # Get buy/sell based on support and resistance levels
    prices = get_historical_prices(symbol, period)
    support = min(prices)
    resistance = max(prices)
    if int(prices[len(prices)-1]) <= support:
        buy+=1
    elif int(prices[len(prices)-1]) >= resistance:
        sell+=1

    if buy >= sell:
        return "Buy"
    else:
        return "Sell"


# Function for getting openai advice on whether to sell or buy
def get_gpt_trade_advice(symbol_name, period=14):
    """
    Function for getting openai advice on whether to sell or buy
    :param symbol_name: Symbol to calculate advice
    :return: Buy/Sell suggestions
    """
    # Gets all the exchange pairs
    exchange_info = client.get_exchange_info()
    trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols']]
    # Checks for invalid user pair
    if symbol_name not in trading_pairs:
        return "Invalid symbol name."

    # Get all the data to give openai for calculations
    symbol = client.get_symbol_info(symbol=symbol_name)
    market_depth = get_average_order_values(symbol=symbol_name)
    recent_trades = get_recent_trade_info(symbol=symbol_name, limit=10)
    recent_prices = get_historical_prices(symbol['symbol'], period)

    # Calculate
    tradeAdvice = gptTradeAdvice(symbol["symbol"], period, recent_prices, recent_trades, market_depth).capitalize()

    return tradeAdvice