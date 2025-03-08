from binance.client import Client
import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime



from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

client = Client()
tr = client.get_historical_trades(symbol = "BTCUSDT", limit=10)
print(tr)


symbol_info = client.get_symbol_info(symbol='BTCUSDT')
print(symbol_info)

def unix_to_date(unix):
    unixTime = int(unix)
    return datetime.fromtimestamp(unixTime/ 1000).strftime('%Y-%m-%d %H:%M:%S')

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

def format_symbol_info(symbol_name):
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
    response = f"Symbol: {symbol['symbol']}\n Status: {symbol['status']}\n Price: {last_price['price']}\n\n Current market: \n {market_depth}\n\n Recent trades: {recent_trades}\n "
    return response



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

def plot_price_in_time(symbol):
    klines = client.get_historical_klines(symbol = symbol, interval = client.KLINE_INTERVAL_1HOUR, start_str ="7 days ago")
    timestamps = []
    closingPrices = []
    for i in range(len(klines)):
        currentKline = klines[i]
        curTime = unix_to_date(int(currentKline[6]))
        timestamps.append(curTime)
        closingPrices.append(float(currentKline[4]))

    plt.plot(timestamps, closingPrices)
    plt.show()
#plot_price_in_time("BTCUSDT")


def get_closing_prices(klines):
    """
    Functiob to extract closing prices from given kline list
    :param klines: List of kline data
    :return: list of closing prices
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

def get_ema(symbol, emaDays, smaDays):
    """
    Function for calculating EMA for given days
    :param symbol: The symbol for calculating the ema of
    :param emaDays: The number of days for ema calculations
    :param smaDays: The number of days for calculating the starting SMA
    :return: List of EMAs of given symbol over the span of given days
    """
    # Get the klines
    klines = client.get_historical_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, start_str=f"{emaDays} days ago")
    # Extract the closing prices
    closePrices = get_closing_prices(klines)
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
    return emas

ts = get_ema("BTCUSDT", 7, 14)
print(ts)


