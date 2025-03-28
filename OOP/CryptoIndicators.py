import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import json
import math
import io

from binance.client import Client

from AiFunctions import AI
from UtilsFunctions import Utils

from DataframeFunctions import Dataframe
from PlotFunctions import Plot
from DatabaseFunctions import MongoDB

class Crypto:
    def __int__(self, Client, AI, Utils, Indicators, Plot, Dataframe):
        self.client = Client()
        self.ai = AI()
        self.utils = Utils()
        self.indicators = Indicators()
        self.plot = Plot()
        self.dataframe = Dataframe()


    # Function for getting specific data from given klines
    def get_data_from_klines(self, klines, desiredData):
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
    def get_average_order_values(self, symbol, limit=20, dictionary=False):
        """
        Function for calculating the average order values for given symbol
        :param symbol:
        :return : Average prices and quantities of bids and asks
        """
        orders = self.client.get_order_book(symbol=symbol, limit=limit)
        bids = orders['bids']  # buy orders
        asks = orders['asks']  # sell order

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

        if dictionary:
            data = {
                "bids": bids,
                "asks": asks,
                "averageAskPrice": averageSellPrice,
                "averageBidPrice": averageBuyPrice,
                "averageAskQuantity": averageSellQuantity,
                "averageBidQuantity": averageBuyQuantity,
            }
            return data

        response = f"Average offered price: {averageSellPrice}\n Average offered quantity: {averageSellQuantity}\n Average asked price: {averageBuyPrice}\n Average asked quantity: {averageBuyQuantity}"
        return response

    # Function for getting info about recent trades of given symbol including the average price and quantity
    def get_recent_trade_info(self, symbol, limit, dictionary=False):
        """
        Function for getting info about recent trades of given symbol including the average price and quantity
        :param symbol: symbol to get recent trades for
        :param limit: limit of records
        :param dictionary: if true function returns dictionary with the data
        :return : Average, minimal and maximal prices and quantities of trades
        """
        trades = self.client.get_recent_trades(symbol=symbol, limit=limit)
        tradeQuantities = []
        tradePrices = []
        totalTradePrice = 0
        for i in range(len(trades)):
            tradeQuantities.append(float(trades[i]['qty']))
            tradePrices.append(float(trades[i]['price']))
            totalTradePrice += float(trades[i]['qty']) * float(trades[i]['price'])

        averageTradeQuantity = (sum(tradeQuantities) / len(tradeQuantities))
        averageTradeQuantity = f"{averageTradeQuantity:.8f}"
        averageTradePrice = (sum(tradePrices) / len(tradePrices))
        MaxTradePrice = max(tradePrices)
        MinTradePrice = min(tradePrices)
        MaxTradeQuantity = min(tradeQuantities)
        MaxTradeQuantity = f"{MaxTradeQuantity:.8f}"
        MinTradeQuantity = min(tradeQuantities)
        MinTradeQuantity = f"{MinTradeQuantity:.8f}"
        totalTradeQuantity = sum(tradeQuantities)
        listTradePrice = sum(tradePrices)

        if dictionary:
            data = {
                "tradeVolume": totalTradeQuantity,
                "priceVolume": totalTradePrice,
                "averageTradeQuantity": averageTradeQuantity,
                "averageTradePrice": averageTradePrice,
                "maxTradePrice": MaxTradePrice,
                "minTradePrice": MinTradePrice,
                "maxTradeQuantity": MaxTradeQuantity,
                "minTradeQuantity": MinTradeQuantity
            }
            return data

        formatedString = f'Average trade quantity: {averageTradeQuantity}\n Average trade price: {averageTradePrice}\n Minimum trade price: {MinTradePrice}\n Maximum trade price: {MaxTradePrice}\n Minimun trade quantity: {MinTradeQuantity}\n Maximum trade quantity: {MaxTradeQuantity}\n'
        return formatedString

    # Function for getting prices of given symbol over the last period days
    def get_historical_prices(self, symbol, period):
        """
        Function for getting prices of given symbol over the last period days
        :param symbol: symbol to get prices of
        :param period: span of days to track
        :return: list of prices
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"{period} days ago")
        closingPrices = self.get_data_from_klines(klines, "Close price")
        return closingPrices

    # Function for showing basic info about given symbol
    def format_symbol_info(self, symbol_name, period=14):
        """
        Function for showing basic info about given symbol
        :param symbol_name:
        :return: Info
        """
        # Gets all the exchange pairs
        exchange_info = self.client.get_exchange_info()
        trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols']]
        # Checks for invalid user pair
        if symbol_name not in trading_pairs:
            return "Invalid symbol name."
        # Returns the info about the symbol
        symbol = self.client.get_symbol_info(symbol=symbol_name)
        # Returns the last price of symbol
        last_price = self.client.get_symbol_ticker(symbol=symbol_name)
        # Get the market state of the symbol
        market_depth = self.get_average_order_values(symbol=symbol_name)
        # Get recent trades of symbol
        recent_trades = self.get_recent_trade_info(symbol=symbol_name, limit=10)
        # Get recent prices
        recent_prices = self.get_historical_prices(symbol['symbol'], period)

        tradeAdvice = self.ai.gptTradeAdvice(symbol["symbol"], period, recent_prices, recent_trades, market_depth).capitalize()

        response = f"Symbol: {symbol['symbol']}\n Status: {symbol['status']}\n Price: {last_price['price']}\n Trade advice: {tradeAdvice}\n\n Current market: \n {market_depth}\n\n Recent trades: \n {recent_trades}\n "
        return response

    # Function to extract closing prices from given kline list
    def get_closing_prices(self, klines):
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

    # Function for getting the current price of given symbol
    def current_price(self, symbol):
        """
        Function for getting the current price of given symbol
        :param symbol: Symbol to calculate current price
        :return: Current price
        """
        symbolPrice = self.client.get_symbol_ticker(symbol=symbol)
        return symbolPrice["price"]

    # Function for getting the recent traded volume of given symbol
    def get_recent_traded_volume(self, symbol, period):
        """
        Function for getting the recent traded volume of given symbol
        :param symbol: Symbol to calculate recent traded volume
        :param period: Period of time for calculation
        :return: Traded volume
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"{period} days ago")
        volumes = self.get_data_from_klines(klines, "Volume")
        volume = sum(volumes)
        return volume

    # Function for getting the number of recent trades of given symbol
    def get_number_of_recent_trades(self, symbol, period):
        """
        Function for getting the number of recent trades of given symbol
        :param symbol: Symbol to calculate number of recent trades
        :param period: Period of time for calculation
        :return: Number of recent trades
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"{period} days ago")
        Trades = self.get_data_from_klines(klines, "Number of trades")
        tradeNumber = sum(Trades)
        return tradeNumber

    # Function for getting the latest price trend
    def get_recent_trend(self, symbol, period):
        """
        Function for getting the recent trend of given symbol
        :param symbol: Symbol to calculate recent trend
        :param period: Period of time for calculation
        :return: Trend
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"1 hour ago")
        openingPrice = self.get_data_from_klines(klines, "Open price")
        closingPrice = self.get_data_from_klines(klines, "Close price")
        trend = self.indicators.get_price_trend(float(openingPrice[0]), float(closingPrice[0]))
        return trend

    def trade_advice(self, symbol, period):
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
        rsi = self.indicators.get_rsi(symbol)
        if rsi > 70:
            sell += 1
        elif rsi < 30:
            buy += 1

        # Get buy/sell based od kdj
        kdj = self.dataframe.get_kdj_dataframe(symbol, period, df=True)
        signals = []

        for i in range(1, len(kdj)):
            if kdj["K"][i] > kdj["D"][i] and kdj["K"][i - 1] <= kdj["D"][i - 1] and kdj['J'][i] > 20 and kdj['J'][
                i - 1] <= kdj['J'][i]:
                signals.append("buy")
            elif kdj['K'][i] < kdj['D'][i] and kdj['K'][i - 1] >= kdj['D'][i - 1] and kdj['J'][i] < 80 and kdj['J'][
                i - 1] >= kdj['J'][i]:
                signals.append("sell")
        if signals[len(signals) - 1] == "buy":
            buy += 1
        else:
            sell += 1

        # Get buy/sell based on support and resistance levels
        prices = self.get_historical_prices(symbol, period)
        support = min(prices)
        resistance = max(prices)
        if int(prices[len(prices) - 1]) <= support:
            buy += 1
        elif int(prices[len(prices) - 1]) >= resistance:
            sell += 1

        if buy >= sell:
            return "Buy"
        else:
            return "Sell"

    # Function for getting openai advice on whether to sell or buy
    def get_gpt_trade_advice(self, symbol_name, period=14):
        """
        Function for getting openai advice on whether to sell or buy
        :param symbol_name: Symbol to calculate advice
        :return: Buy/Sell suggestions
        """
        # Gets all the exchange pairs
        exchange_info = self.client.get_exchange_info()
        trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols']]
        # Checks for invalid user pair
        if symbol_name not in trading_pairs:
            return "Invalid symbol name."

        # Get all the data to give openai for calculations
        symbol = self.client.get_symbol_info(symbol=symbol_name)
        market_depth = self.get_average_order_values(symbol=symbol_name)
        recent_trades = self.get_recent_trade_info(symbol=symbol_name, limit=10)
        recent_prices = self.get_historical_prices(symbol['symbol'], period)

        # Calculate
        tradeAdvice = self.ai.gptTradeAdvice(symbol["symbol"], period, recent_prices, recent_trades, market_depth).capitalize()

        return tradeAdvice

    # Function for calculating weighted average
    def calculate_weighted_average(self, data):
        """
        Function for calculating weighted average
        :param data: data to calculate weighted average of
        :return: weighted average
        """
        totalValue = 0
        totalQuantity = 0

        for price, quantity in data:
            price = float(price)
            quantity = float(quantity)
            totalValue += price * quantity
            totalQuantity += quantity

        if totalQuantity == 0:
            return 0

        return totalValue / totalQuantity


    # Function for updating the state of users crypto balance in db
    def update_balance(self, symbol, userId, amount, action):
        """
        Function for updating the state of users crypto balance in db
        :param symbol: symbol for choosing which record to update
        :param userId: id of the user
        :param amount: amount for the update
        :param action: action to do
        :return: response
        """
        # Check for invalid action
        if action not in ["remove", "add"]:
            return "Invalid action"

        db = MongoDB()
        # Get users data for given symbol
        selectQuery = {"userId": userId, "symbol": symbol}
        selectResponse = list(db.select(query=selectQuery, col="Usercrypto"))

        # Check if any record exists
        if len(selectResponse) == 0:
            if action == "remove":
                return "No resources for given symbol"
            else:
                # If the record doesnt exist and the action is "add" create new record
                insertQuery = self.utils.formatInsertQuery(format="balance", func="baance", userId=userId, symbol=symbol,
                                                amount=amount)
                insertResponse = db.insert(col="Usercrypto", query=insertQuery)
                return "Successfuly updated"

        # Get the record data
        currentAmount = selectResponse[0]["amount"]
        recordId = selectResponse[0]["_id"]
        newAmount = 0

        # Get new amount
        if action == "remove":
            if amount > currentAmount:
                return "Invalid amount"
            newAmount = currentAmount - amount
        elif action == "add":
            newAmount = currentAmount + amount

        # Update the record
        updateQuery = self.utils.formatUpdateQuery(format="balance", amount=newAmount)
        updateResponse =db.update(col="Usercrypto", postId=recordId, values=updateQuery)
        db.close()
        return updateResponse

    def get_balance_worth(self, userId, symbol=None, dictionary=None):
        """
        Function for getting users wallet data and their worth
        :param userId: id of user
        :param symbol: optional symbol to look for
        :param dictionary: if true returns dictionary with data
        :return: formatted user wallet data
        """
        db = MongoDB()
        if symbol:
            selectQuery = {"userId": userId, "symbol": symbol.upper()}
            response = list(db.select(query=selectQuery, col="Usercrypto"))
            if len(response) == 0:
                return "No data found for given symbol"
        else:
            selectQuery = {"userId": userId}
            response = list(db.select(query=selectQuery, col="Usercrypto"))
            if len(response) == 0:
                return "No data found"

        if dictionary:
            responseDict = self.utils.formatBalanceResponse(data=response, dictionary=True)
            for i in responseDict.values():
                currentPrice = self.current_price(i["symbol"])
                i["value"] = float(currentPrice) * float(i["amount"])
            return responseDict

        formatedResponse = ""
        for i in response:
            symbolPrice = self.current_price(i["symbol"])
            formatedStr = f"Your wallet:\n\nsymbol: {i['symbol']}\namount: {i['amount']}\nvalue: {float(symbolPrice) * float(i['amount'])}"
            formatedResponse = formatedResponse + formatedStr

        db.close()
        return formatedResponse

    # Function for registering a new user
    def register_user(self, userId):
        """
        Function for registering a new user
        :param userId: id of the user
        :return:
        """
        db = MongoDB()
        # Check if user isnt already registered
        selectQuery = {"userId": userId}
        selectResponse = list(db.select(query=selectQuery, col="Users"))

        # If he isnt register him
        if len(selectResponse) == 0:
            insertQuery = self.utils.formatInsertQuery(format="user", userId=userId)
            db.insert(col="Users", query=insertQuery)
        db.close()

class Indicators:
    def __init__(self):
        self.client = Client()
        self.crypto = Crypto()
        self.utils = Utils()

    # Function for getting mfi of given symbol
    def get_mfi(self, symbol, period=14):
        """
        Function for getting mfi of given symbol
        :param symbol: symbol to calculate mfi of
        :param period: period of mfi
        :return: mfi
        """
        # Get the price data
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"{period} days ago")
        openingPrices = self.crypto.get_data_from_klines(klines = klines, desiredData="Open price")
        closingPrices = self.crypto.get_data_from_klines(klines, "Close price")
        highPrices = self.crypto.get_data_from_klines(klines, "High price")
        lowPrices = self.crypto.get_data_from_klines(klines, "Low price")
        volumes = self.crypto.get_data_from_klines(klines, "Volume")
        timestamps = self.crypto.get_data_from_klines(klines, "Close time")

        # Calculate TPs
        TPs = []
        rawMoneyFlows = []
        negativeMoneyFlow = 0
        positiveMoneyFlow = 0
        for i in range(len(closingPrices)):
            # Calculate tp
            tp = (highPrices[i] + lowPrices[i] + closingPrices[i]) / 3
            TPs.append(tp)
            # Calculate raw money flow
            rawMoneyFlow = tp * volumes[i]
            rawMoneyFlows.append(rawMoneyFlow)

        # Sort the raw money flows to positive or negatives
        for i in range(1, len(TPs)):
            if TPs[i] > TPs[i - 1]:
                positiveMoneyFlow += rawMoneyFlows[i]
            elif TPs[i] < TPs[i - 1]:
                negativeMoneyFlow += rawMoneyFlows[i]

        # Calculate money flow ratio
        MFR = positiveMoneyFlow / negativeMoneyFlow

        # Calculate money flow index
        MFI = 100 - (100 / (1 + MFR))

        return MFI

    # Function for getting atr of given symbol
    def get_atr(self, symbol, period=30, dictionary=False):
        """
        Function for getting atr of given symbol
        :param symbol: symbol to calculate atr of
        :param period: period of atr
        :param dictionary: if true returns dictionary with more data
        :return: final atr over the last period/30 days
        """
        InitialRTAPeriod = 14

        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{period + 1} days ago")
        closingPrices = self.crypto.get_data_from_klines(klines, "Close price")
        highPrices = self.crypto.get_data_from_klines(klines, "High price")
        lowPrices = self.crypto.get_data_from_klines(klines, "Low price")

        InitialTRs = []
        TRs = []
        ATRs = []

        for i in range(1, len(closingPrices)):
            # Calculate TR
            TR = max(highPrices[i] - lowPrices[i], abs(highPrices[i] - closingPrices[i - 1]),
                     abs(lowPrices[i] - closingPrices[i - 1]))
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
            ATR = (ATR * (InitialRTAPeriod - 1) + TRs[i]) / InitialRTAPeriod
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

    # Function for getting 14 day rsi for symbol
    def get_rsi(self, symbol):
        """
        Function for getting RSI of given symbol
        :param symbol: The symbol to get RSI
        :return: The RSI of the symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str="15 days ago")
        closePrices = self.crypto.get_closing_prices(klines)
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
            rsi = 100 - (100 / (1 + rs))

        return rsi

    # Function for calculating SMA of given symbol in the range of given days
    def get_sma(self, symbol, days):
        """
        Function for calculating SMA of given symbol in the range of given days
        :param symbol: The symbol for calculating the sma of
        :param days: The number of days for calculations
        :return: SMA of given symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{days + 1} days ago")
        closePrices = self.crypto.get_closing_prices(klines)
        sma = sum(closePrices) / len(closePrices)
        return sma

    # Function for calculating EMA for given days
    def get_ema(self, symbol, emaDays=14, smaDays=10, timestamp=False):
        """
        Function for calculating EMA for given days
        :param symbol: The symbol for calculating the ema of
        :param emaDays: The number of days for ema calculations
        :param smaDays: The number of days for calculating the starting SMA
        :param timestamp: Flag for checking if you want to also return corresponding timestamps
        :return: List of EMAs of given symbol over the span of given days
        """
        # Get the klines
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{emaDays} days ago")
        # Extract the closing prices
        closePrices = self.crypto.get_closing_prices(klines)
        timestamps = self.crypto.get_data_from_klines(klines, "Close time")
        # Get SMA
        sma = self.get_sma(symbol, smaDays)
        alpha = 2 / (emaDays + 1)
        emas = []
        # Get the EMAs
        for i in range(len(closePrices)):
            currentPrice = closePrices[i]
            if len(emas) == 0:
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
    def get_kdj(self, symbol, period):
        """
        Function for calculating KDJ for given symbol over the given period of time
        :param symbol: Symbol to calculate KDJ of
        :param period: Period of time for calculation
        :return:
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{period} days ago")
        closePrices = self.crypto.get_data_from_klines(klines, "Close price")
        highPrices = self.crypto.get_data_from_klines(klines, "High price")
        lowPrices = self.crypto.get_data_from_klines(klines, "Low price")
        closeTimes = self.crypto.get_data_from_klines(klines, "Close time")
        # Lists for the KDJs
        Ks = []
        Ds = []
        Js = []
        for i in range(period):
            # Lowest prices till the day
            low = lowPrices[:(i + 1)]
            # Highest prices till the day
            high = highPrices[:(i + 1)]
            close = closePrices[i]
            # Calculate the K
            K = (close - min(low)) / (max(high) - min(low)) * 100
            Ks.append(K)
            # If you have K data from more than 3 days calculate the other metrics
            if len(Ks) > 2:
                # Get last three Ks
                lastThreeKs = Ks[-3:]
                # Calcutale the D
                D = sum(lastThreeKs) / len(lastThreeKs)
                Ds.append(D)
                # Calculate the J
                J = 3 * K - 2 * D
                Js.append(J)
            else:
                Ds.append(0)
                Js.append(0)
        for i in range(len(closeTimes)):
            closeTimes[i] = self.utils.unix_to_date(int(closeTimes[i]), day=True)
        return Ks, Ds, Js, closeTimes

    # Function for calculating bollinger lines for given symbol over given period of time
    def get_boll(self, symbol, period=14, dictionary=False):
        """
        Function for calculating bollinger lines for given symbol over given period of time
        :param symbol: symbol for calculating the bollinger of
        :param period: period of time for calculation
        :param dictionary: if true return dictionary with data
        :return: mb, ub, lb lines
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{period} days ago")
        closePrices = self.crypto.get_closing_prices(klines)
        SMA = sum(closePrices) / len(closePrices)
        MB = SMA

        # Calculate the sum of differences
        differenceSum = 0
        for i in range(len(closePrices)):
            differenceSum += (closePrices[i] - SMA) ** 2
        # Calculate standard deviation
        SD = math.sqrt((differenceSum) / len(closePrices))
        # Calculate lower and upper bands
        UB = SMA + (2 * SD)
        LB = SMA - (2 * SD)

        if dictionary:
            data = {
                "MB": MB,
                "UB": UB,
                "LB": LB,
                "SD": SD
            }
            return data
        return MB, UB, LB

    # Function for calculating AVL of given symbol over given period of time
    def get_avl(self, symbol, period=14):
        """
        Function for calculating AVL of given symbol over given period of time
        :param symbol: symbol for calculating the AVL of
        :param period: period of time for calculation
        :return: AVL of given symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{period} days ago")
        # Get the trade volumes
        volumes = self.crypto.get_data_from_klines(klines, "Volume")
        # Calculate AVL
        AVL = sum(volumes) / len(volumes)
        return AVL

    # Function for calculating liquidity for given symbol over given period of time
    def get_liquidity(self, symbol, period=1, dictionary=False):
        """
        Function for calculating liquidity for given symbol over given period of time
        :param symbol: symbol for calculating the liquidity
        :param period: period of time for calculation
        :param dictionary: if true return dictionary with data
        :return: liquidity of given symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1DAY,
                                              start_str=f"{period} days ago")
        # Get bid-ask spread
        baSpread = self.get_bid_ask_spread(symbol, limit=100)

        if baSpread <= 0:
            return 0
        # Get the traded volume
        tradedVolume = sum(self.crypto.get_data_from_klines(klines, "Volume"))
        # Calculate liquidity
        liquidity = tradedVolume / baSpread

        if dictionary:
            data = {
                "baSpread": baSpread,
                "tradedVolume": tradedVolume,
                "liquidity": liquidity
            }
            return data

        return liquidity

    # Function for getting cci of given symbol
    def get_cci(self, symbol, period, timestamp=False):
        """
        Function for getting cci of given symbol
        :param symbol: symbol to calculate cci of
        :param period: period of cci
        :param timestamp: if true returns cci data + timestamp
        :return: CCI data
        """
        # Get the price data
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"{period} days ago")
        openingPrices = self.crypto.get_data_from_klines(klines, "Open price")
        closingPrices = self.crypto.get_data_from_klines(klines, "Close price")
        highPrices = self.crypto.get_data_from_klines(klines, "High price")
        lowPrices = self.crypto.get_data_from_klines(klines, "Low price")
        timestamps = self.crypto.get_data_from_klines(klines, "Close time")

        TPs = []
        absoluteDifferences = []
        CCIs = []
        for i in range(len(closingPrices)):
            # Calculate TP
            tp = (highPrices[i] + lowPrices[i] + closingPrices[i]) / 3
            TPs.append(tp)

        # Calculate SMA
        SMA = sum(TPs) / len(TPs)
        for i in range(len(TPs)):
            absoluteDifferences.append(abs(TPs[i] - SMA))

        # Calculate mean absolute deviation
        MAD = sum(absoluteDifferences) / len(absoluteDifferences)

        # Calculate CCI for each day
        for i in range(len(TPs)):
            cci = (TPs[i] - SMA) / (0.015 * MAD)
            CCIs.append(cci)

        if timestamp:
            return CCIs, timestamps

        return CCIs

    # Function for getting bid-ask spread of given symbol
    def get_bid_ask_spread(self, symbol, limit=100, dictionary=False):
        """
        Function for getting bid-ask spread of given symbol
        :param symbol: symbol to calculate spread
        :param limit: limit of orders evaluated
        :param dictionary: if true returns dictionary of all the values including average bid and ask weighted averages
        :return: bid-ask spread
        """
        orderData = self.crypto.get_average_order_values(symbol=symbol, limit=limit, dictionary=True)
        bids = orderData['bids']
        asks = orderData['asks']

        bidAverage = self.crypto.calculate_weighted_average(bids)
        askAverage = self.crypto.calculate_weighted_average(asks)

        spread = bidAverage - askAverage

        if spread < 0:
            spread = 0

        if dictionary:
            data = {
                "averageBid": bidAverage,
                "averageAsk": askAverage,
                "spread": spread
            }
            return data

        return spread

    # Function for getting order book imbalance of given symbol
    def get_order_book_imbalance(self, symbol, limit=100, dictionary=False):
        """
        Function for getting order book imbalance of given symbol
        :param symbol: symbol to calculate imbalance of
        :param limit: limit for the order data
        :param dictionary: if true return dictionary with data
        :return: imbalance
        """
        # Get the order data
        orderData = self.crypto.get_average_order_values(symbol=symbol, limit=limit, dictionary=True)
        bids = orderData['bids']
        asks = orderData['asks']
        # Calculate bid and ask volumes
        totalBuy = sum(float(quantity) for price, quantity in bids)
        totalSell = sum(float(quantity) for price, quantity in asks)
        # Calculate imbalance
        imbalance = (totalBuy - totalSell) / (totalBuy + totalSell) * 100

        if dictionary:
            data = {
                "bidVolume": totalBuy,
                "askVolume": totalSell,
                "imbalance": imbalance
            }
            return data

        return imbalance

    # Function for getting volatility percentage of given symbol over the span of given days
    def get_volatility(self, symbol, period, average=False, timestamp=False):
        """
        Function for getting volatility percentage of given symbol over the span of given days
        :param symbol: symbol to calculate volatility of
        :param period: number of days for measuring
        :param average: If true functions returns average volatility
        :param timestamp: If true functions returns volatilities+corresponding timestamps
        :return: list of daily volatilities and timestamps
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                              start_str=f"{period} days ago")
        openingPrices = self.crypto.get_data_from_klines(klines, "Open price")
        highPrices = self.crypto.get_data_from_klines(klines, "High price")
        lowPrices = self.crypto.get_data_from_klines(klines, "Low price")
        timestamps = self.crypto.get_data_from_klines(klines, "Close time")
        percentageVolatilities = []
        for i in range(len(openingPrices)):
            volatilityPercentage = (highPrices[i] - lowPrices[i]) / openingPrices[i] * 100
            percentageVolatilities.append(volatilityPercentage)

        if average:
            return sum(percentageVolatilities) / len(percentageVolatilities)

        if timestamp:
            return percentageVolatilities, timestamps

        return percentageVolatilities

    # Function for getting the market pattern base on the opening and closing price
    def get_price_trend(self, openingPrice, closingPrice):
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