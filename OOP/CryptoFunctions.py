class Crypto:
    def __init__(self, Client, AI, Utils, Indicators, Plot, Dataframe):
        self.client = Client
        self.ai = AI
        self.utils = Utils
        self.indicators = Indicators
        self.plot = Plot
        self.dataframe = Dataframe

    @staticmethod
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

    @staticmethod
    # Function to extract closing prices from given kline list
    def get_closing_prices(klines):
        """
        Function to extract closing prices from given klines
        :param klines: List of kline data
        :return: List of closing prices
        """
        closingPrices = []
        for i in range(len(klines)):
            currentKline = klines[i]
            closingPrices.append(float(currentKline[4]))
        return closingPrices

    @staticmethod
    # Function for calculating weighted average
    def calculate_weighted_average(data):
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

    # Function for calculating the average order values for given symbol
    def get_average_order_values(self, symbol, limit=20, dictionary=False):
        """
        Function for calculating the average order values
        :param symbol: Symbol to calculate order values of
        :param limit: Limit of order values
        :param dictionary: Boolean to use dictionary or not
        :return : Average prices and quantities of bids and asks
        """
        orders = self.client.get_order_book(symbol=symbol, limit=limit)
        bids = orders['bids']  # buy orders
        asks = orders['asks']  # sell order

        # Calulate the averages
        averageBuyPrice, averageBuyQuantity = self.utils.format_order_data(data=bids)
        averageSellPrice, averageSellQuantity = self.utils.format_order_data(data=asks)

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
        #response = f"Average offered price💸: {averageSellPrice}\n Average offered quantity📦: {averageSellQuantity}\n Average asked price💵: {averageBuyPrice}\n Average asked quantity📦: {averageBuyQuantity}"
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
        #formatedString = f'Average trade quantity⚖️📦: {averageTradeQuantity}\n Average trade price⚖️💰: {averageTradePrice}\n Minimum trade price⬇️💰: {MinTradePrice}\n Maximum trade price⬆️💰: {MaxTradePrice}\n Minimun trade quantity⬇️📦: {MinTradeQuantity}\n Maximum trade quantity⬆️📦: {MaxTradeQuantity}\n'
        formatedString = f'Average trade quantity: {averageTradeQuantity}\n Average trade price: {averageTradePrice}\n Minimum trade price: {MinTradePrice}\n Maximum trade price: {MaxTradePrice}\n Minimun trade quantity: {MinTradeQuantity}\n Maximum trade quantity: {MaxTradeQuantity}\n'
        return formatedString

    # Function for getting prices of given symbol over the last period days
    def get_historical_prices(self, symbol, period, interval="1h"):
        """
        Function for getting prices of given symbol over the last period days
        :param symbol: symbol to get prices of
        :param period: span of days to track
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: list of prices
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval,
                                              start_str=f"{period} days ago")
        closingPrices = self.get_data_from_klines(klines, "Close price")
        return closingPrices

    # Function for showing basic info about given symbol
    def format_symbol_info(self, symbol_name, period=14, trade_limit = 10):
        """
        Function for showing basic info
        :param symbol_name: symbol to get info about
        :param period: span of days to track
        :param trade_limit: max number of trades to get for the calculation
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
        recent_trades = self.get_recent_trade_info(symbol=symbol_name, limit=trade_limit)
        # Get recent prices
        recent_prices = self.get_historical_prices(symbol['symbol'], period)

        tradeAdvice = self.ai.gptTradeAdvice(symbol["symbol"], period, recent_prices, recent_trades, market_depth).capitalize()

        response = f"Symbol🔣: {symbol['symbol']}\n Status🟢: {symbol['status']}\n Price💸: {last_price['price']}\n Trade advice💡: {tradeAdvice}\n\n Current market🏦: \n {market_depth}\n\n Recent trades🕒: \n {recent_trades}\n "
        return response

    # Function for getting the current price of given symbol
    def current_price(self, symbol):
        """
        Function for getting the current price
        :param symbol: Symbol to calculate price of
        :return: Current price
        """
        symbolPrice = self.client.get_symbol_ticker(symbol=symbol)
        return symbolPrice["price"]

    # Function for getting the recent traded volume of given symbol
    def get_recent_traded_volume(self, symbol, period, interval="1h"):
        """
        Function for getting the recent traded volume
        :param symbol: Symbol to calculate recent traded volume
        :param period: Period of time for calculation
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: Traded volume
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
        volumes = self.get_data_from_klines(klines, "Volume")
        volume = sum(volumes)
        return volume

    # Function for getting the number of recent trades of given symbol
    def get_number_of_recent_trades(self, symbol, period, interval="1h"):
        """
        Function for getting the number of recent trades
        :param symbol: Symbol to calculate number of recent trades
        :param period: Period of time for calculation in days
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: Number of recent trades
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
        Trades = self.get_data_from_klines(klines, "Number of trades")
        tradeNumber = sum(Trades)
        return tradeNumber

    # Function for getting the latest price trend
    def get_recent_trend(self, symbol, period=1, interval="1h"):
        """
        Function for getting the recent trend
        :param symbol: Symbol to calculate recent trend
        :param period: Period of time for calculation in hours
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: Trend
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval,
                                              start_str=f"{period} hour ago")
        openingPrice = self.get_data_from_klines(klines, "Open price")
        closingPrice = self.get_data_from_klines(klines, "Close price")
        trend = self.indicators.get_price_trend(float(openingPrice[0]), float(closingPrice[0]))
        return trend

    # Function for calculating custom trade advice
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
        :param period: Period of time for calculation
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
