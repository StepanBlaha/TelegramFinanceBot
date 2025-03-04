from binance.client import Client

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

client = Client()
tr = client.get_historical_trades(symbol = "BTCUSDT", limit=10)
print(tr)


symbol_info = client.get_symbol_info(symbol='BTCUSDT')
print(symbol_info)

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

