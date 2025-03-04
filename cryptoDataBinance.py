#pip install python-binance
from binance.client import Client
from datetime import datetime
import time

# initializnu clienta
client = Client()
 # .get_ymbol_ticker(symbol=) bere jako symbol 2tagy porovnananych hodnot
price = client.get_symbol_ticker(symbol="BTCUSDT")
print(price)

info = client.get_symbol_info('BNBBTC')
print(info)







#------------------------------------------------------------------------------------------------------------------------------------------

#Vypise posledni cenu vsech aktiv
tickers = client.get_all_tickers()
print(tickers)



#------------------------------------------------------------------------------------------------------------------------------------------

#Najde detaily o mene/ aktivu
#get_asset_details()

#------------------------------------------------------------------------------------------------------------------------------------------
#-----z tohohle bych mohl udelat graf kolik transakci probehlo za poslednich 24h a v jakem prumeru hodnoty
# vypise vsechny trady od nejakeho casu do ted
trades = client.aggregate_trade_iter(symbol="BTCUSDT", start_str="5 minutes ago UTC")
# vraci v generatoru - musim projet loopem
#for trade in trades:
 #   print(trade)  # Each trade is a JSON object
#------------------------------------------------------------------------------------------------------------------------------------------
# vypise prumernou cenu aktiva za poslednich 5 minut
avg = client.get_avg_price(symbol="BTCUSDT")
print(avg)

#------------------------------------------------------------------------------------------------------------------------------------------
# vypise list trading paru s mnoha daty - asi nikde nevyuziju
ex = client.get_exchange_info()
#print(ex)
#------------------------------------------------------------------------------------------------------------------------------------------
# vezme svickovy data daneho aktiva v intervalu (vezme jakoby svicku vzdy za interval, tady jednou za hodinu), od startovniho intervalu, optional limit- limit svicek co budm mit- default je 500, muze byt i end time [end_str], optionel je jeste klines_type tedy jaky chceme typ svicek
# dava vraci takto :
#[
#    [timestamp, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore]
#]
kl = client.get_historical_klines("BNBBTC", client.KLINE_INTERVAL_1HOUR, start_str=" 3 hours ago")
#print(kl)

# je pak i get_historical_klines_generator() - ktery misto listu vraci generator- musim prochazet loopem
#------------------------------------------------------------------------------------------------------------------------------------------
# vraci jednotlive trady bere symbol a limit poctu
tr = client.get_historical_trades(symbol = "BTCUSDT", limit=10)

#------------------------------------------------------------------------------------------------------------------------------------------
# vrati data jako symbol, stepsize, quantity, atd.. o jednotlivem aktivu
singleSymbolData = client.get_isolated_margin_symbol(symbol = "BTCUSDT")

#------------------------------------------------------------------------------------------------------------------------------------------

#PRAKTCKY stejny jako to get_historical_klines
singleSymbolKlines = client.get_klines(symbol = "BTCUSDT", interval = client.KLINE_INTERVAL_1HOUR, limit = 500, start_str=" 3 hours ago")


#------------------------------------------------------------------------------------------------------------------------------------------
#vrati list otevrenych nabidek a poptavek pro dane aktivum
activeOrders = client.get_order_book(symbol="BTCUSDT", limit = 5)
#------------------------------------------------------------------------------------------------------------------------------------------
# vrati nejvyssi popavku, nejlevnejsi nabdku a posledni prodanou cenu pto aktivum
Ordertick = client.get_orderbook_ticker(symbol="BTCUSDT")
#------------------------------------------------------------------------------------------------------------------------------------------
# vrati trading pary
exchange_info = client.get_exchange_info()
#------------------------------------------------------------------------------------------------------------------------------------------
#vrati posledni trady pro dany symbol
recent_trades = client.get_recent_trades(symbol='BTCUSDT', limit=5)
#------------------------------------------------------------------------------------------------------------------------------------------
# vrati list dostupnych flexibilnich produktu - typ aktiva kde uzivatel dostava intrest a muze kdykoliv withdrawnout
flexible_products = client.get_simple_earn_flexible_product_list()
#------------------------------------------------------------------------------------------------------------------------------------------
# vrati info o symbolu
symbol_info = client.get_symbol_info(symbol='BTCUSDT')
#------------------------------------------------------------------------------------------------------------------------------------------
# vrati posledni cenu pro symbol
symbol_ticker = client.get_symbol_ticker(symbol='BTCUSDT')
# je pak i get_symbol_ticker_window ktery jeste bere window="" napr 5m
#------------------------------------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------------------------
