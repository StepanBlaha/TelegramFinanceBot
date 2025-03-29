class AutoFunc:
    def __init__(self, Client, Crypto, Plot, Dataframe, Indicators):
        self.client = Client
        self.crypto = Crypto
        self.plot = Plot
        self.dataframe = Dataframe
        self.indicators = Indicators

    @staticmethod
    # Function for sending info about price change of given symbol
    async def priceMonitor(params, userId, bot):
        """
        Function for sending info about price change of given symbol
        :param params: list containing data such as symbol and price difference
        :param userId: id of the user
        :param bot: bot
        :return:
        """
        # Get the data
        symbol = params[0]
        priceDiff = params[1]
        percentageDiff = params[2]
        lastPrice = params[3]
        newPrice = lastPrice + priceDiff

        await bot.send_message(chat_id=userId,
                               text=f" ''''''''''''''''''''''''''''Watch out''''''''''''''''''''''''''''\n\nThe price for {symbol} has changed by {percentageDiff}%\n Old price: {lastPrice}\n New price: {newPrice}\n Price change: {priceDiff}")

    async def digest(self, params, userId, bot):
        """
        Function for sending basic infor about the symbol changes
        :param params: list including symbol and period
        :param userId: id of the user
        :param bot: bot
        :return:
        """
        # Get the parameters
        symbol = params[0]
        period = params[1] if len(params) > 1 else 14
        if period == False:
            period = 14

        # Get the base info
        recentPrice = float(self.crypto.current_price(symbol))
        recentTradeVolume = self.crypto.get_recent_traded_volume(symbol, period)
        recentTradeNumber = self.crypto.get_number_of_recent_trades(symbol, period)
        recentTrend = self.crypto.get_recent_trend(symbol, period)
        await bot.send_message(chat_id=userId,
                               text=f"The latest price for {symbol} is: {recentPrice}.\n The traded volume in the last {period} days: {recentTradeVolume}.\n The number of trades made in the last {period} days: {recentTradeNumber}.\n Latest trend: {recentTrend}")

        # Get the price data
        graphPrice = self.plot.plot_price_in_time(symbol, period)
        await bot.send_photo(chat_id=userId, photo=graphPrice)

        # Get the EMA data
        graphEMA = self.plot.plot_ema(symbol, period)
        dataframeEMA = self.dataframe.get_ema_dataframe(symbol, period)

        await bot.send_photo(chat_id=userId, photo=graphEMA)
        await bot.send_message(chat_id=userId, text=f"Here is the EMA data:\n```\n{dataframeEMA}\n```",
                               parse_mode="Markdown")

        # Get the KDJ data
        graphKDJ = self.plot.plot_kdj(symbol, period)
        dataframeKDJ = self.dataframe.get_kdj_dataframe(symbol, period)

        await bot.send_photo(chat_id=userId, photo=graphKDJ)
        await bot.send_message(chat_id=userId, text=f"Here is the KDJ data:\n```\n{dataframeKDJ}\n```",
                               parse_mode="Markdown")

    # Function for sending user personalised update about chosen cryptocurrency
    async def cryptoUpdate(self, symbol, userId, bot, lastPrice, interval):
        """
        Function for sending user personalised update about chosen cryptocurrency
        :param symbol: symbol of cryptocurrency
        :param userId: id of user
        :param bot: telegram bot
        :param lastPrice: last price of cryptocurrency
        :param interval: interval between updates
        :return:
        """
        # rozdil ceny normalne a procentualne, done
        # tradenuto volume done
        # volatilitu done
        # bid-ask spread done
        # order book imbalance done
        #

        currentPrice = float(self.crypto.current_price(symbol))
        priceChange = currentPrice - lastPrice
        percentualChange = (currentPrice - lastPrice) / lastPrice * 100
        await bot.send_message(chat_id=userId,
                               text=f"The latest price for {symbol} is: {currentPrice}.\n Last recorded price: {lastPrice}\n Raw price change: {priceChange}.\n Percentual price change: {percentualChange}%")

        # Get the recent trade data and format them
        tradeData = self.crypto.get_recent_trade_info(symbol=symbol, limit=200, dictionary=True)
        await bot.send_message(chat_id=userId,
                               text=f"Data about recent trades\n\n Total trade volume: {tradeData['tradeVolume']}\n Total trade price: {tradeData['priceVolume']}\n Max trade price: {tradeData['maxTradePrice']}\n Min trade price: {tradeData['minTradePrice']}\n Max trade volume: {tradeData['maxTradeQuantity']}\n Min trade volume: {tradeData['minTradeQuantity']}\n Average trade price: {tradeData['averageTradePrice']}\n Average trade volume: {tradeData['averageTradeQuantity']}")

        # Format the period for volatility into days
        period = interval / 86400
        if period < 1:
            period = 1
        avgPercentVolatility = self.indicators.get_volatility(symbol=symbol, period=period, average=True)
        await bot.send_message(chat_id=userId, text=f"The average percentage volatility: {avgPercentVolatility}%")
        # Get the volatility graph and send it to user
        graphVolatilities = self.plot.plot_volatility(symbol, period)
        await bot.send_photo(chat_id=userId, photo=graphVolatilities)

        bidAskSpreadData = self.indicators.get_bid_ask_spread(symbol=symbol, dictionary=True)
        await bot.send_message(chat_id=userId,
                               text=f"The average bid-ask spread: {bidAskSpreadData['spread']}\n Average bid price: {bidAskSpreadData['averageBid']}\n Average ask price: {bidAskSpreadData['averageAsk']}")

        orderBookImbalance = self.indicators.get_order_book_imbalance(symbol=symbol)
        await bot.send_message(chat_id=userId, text=f"The order book imbalance: {orderBookImbalance}%")
