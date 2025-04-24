# pip install python-telegram-bot --upgrade
# pip install python-binance
# pip install pandas
# pip install matplotlib
# import pymysql
# pip install mysql-connector-python
# pip install pymongo
# python -m pip install "pymongo[srv]"

"""
start - Start interacting with the bot
help - Get help on how to use the bot
symbol_info - Get the base info about a given symbol. (Format: /symbol_info symbol)
price_chart - Get a graph of prices of given symbol over the span of given days. (Format: /price_chart symbol period)
EMA - Get a graph of EMA of given symbol over the span of given days. (Format: /EMA symbol period)
KDJ - Get a graph of KDJ of given symbol over the span of given days. (Format: /KDJ symbol period)
digest - Set a symbol you want to get info about after given interval of time, optionally set the span of days the graphs should be measured. (Format: /digest symbol interval optional days). The interval can be in following format: daily, weekly, monthly, if the given interval is number it is taken as hours
indicators - Get indicator for a desired symbol. (Format: /indicators symbol optional: name of indicator)
monitor - Set monitor for desired symbol, you get notification after certain price change. (Format: /set_monitor symbol margin)
update - Set a monitor to for getting basic info about a symbol after certain period of time. (Format: /crypto_update symbol interval)
my_functions - Show all you set monitors, digests or cryptoupdates. (Format: /my_functions function)
delete - Delete a set monitor, digest or cryptoupdate. (Format: /delete function symbol val(interval/margin)
chatbot - Message a custom chatbot for anything you need. (Format: /chatbot message)
tradeAdvice - Get a trading advice for a symbol. (Format: /tradeAdvice symbol)
balance - Check, add or delete your balance in database for a symbol. (Format: /balance action symbol amount)(actions: add, remove, show, value)











start - Start interacting with the bot
help - Get help on how to use the bot
symbol_info - Get info about a symbol
price_chart - Get price chart for a symbol
ema - Get EMA chart for a symbol
kdj - Get KDJ chart for a symbol
digest - Set digest for a symbol at intervals
indicators - Get indicators for a symbol
monitor - Set a price monitor for a symbol
update - Get periodic updates for a symbol
my_functions - Show all your active functions
delete - Delete a monitor, digest or update
chatbot - Chat with a custom assistant
tradeadvice - Get trade advice for a symbol
balance - Manage your balance for a symbol








@SbFinanceBot
start - Start interacting with the bot
help - Get help on how to use the bot
symbol_info - Get the base info about a given symbol
price_chart - Get a graph of prices of a given symbol over the span of given days
EMA - Get a graph of EMA of a given symbol over the span of given days
KDJ - Get a graph of KDJ of a given symbol over the span of given days
digest - Set a symbol you want to get info about after a given interval of time



import pymysql


pip install python-telegram-bot --upgrade
pip install python-binance
pip install pandas
pip install matplotlib
pip install mysql-connector-python
pip install pymongo
python -m pip install "pymongo[srv]"
pip install google-genai
pip install -q -U google-genai
pip install openai
pip install python-dotenv
pip install requests


pip install -U "steam[client]"




Tests:

/price_chart BTCUSDT 14
/balance add BTCUSDT 13
/indicators BTCUSDT
/chatbot hello
/symbol_info BTCUSDT
/digest BTCUSDT 1 6
/ema BTCUSDT 14





"""