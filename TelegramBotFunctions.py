from binance.client import Client

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

client = Client()
tr = client.get_historical_trades(symbol = "BTCUSDT", limit=10)
print(tr)


symbol_info = client.get_symbol_info(symbol='BTCUSDT')
print(symbol_info)

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
    last_price = client.get_symbol_ticker(symbol=symbol_name)
    response = f"Symbol: {symbol['symbol']}\n Status: {symbol['status']}\n Price: {last_price['price']}\n "
    return response

