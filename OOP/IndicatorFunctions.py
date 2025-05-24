from autoload import *

class Indicators:
    def __init__(self, Client, Crypto, Utils):
        self.client = Client
        self.crypto = Crypto
        self.utils = Utils

    @staticmethod
    # Function for getting the market pattern base on the opening and closing price
    def get_price_trend(openingPrice, closingPrice):
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

    # Function for getting mfi of given symbol
    def get_mfi(self, symbol, period=14, interval="1h"):
        """
        Function for getting mfi of given symbol
        :param symbol: symbol to calculate mfi of
        :param period: period of mfi
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: mfi
        """
        # Get the price data
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval,
                                              start_str=f"{period} days ago")
        _, closingPrices, highPrices, lowPrices, _, volumes = self.utils.format_kline_data(klines=klines)

        # Calculate TPs
        TPs, rawMoneyFlows = [], []
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
    def get_atr(self, symbol, period=30, dictionary=False, interval="1d"):
        """
        Function for getting atr of given symbol
        :param symbol: symbol to calculate atr of
        :param period: period of atr
        :param dictionary: if true returns dictionary with more data
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: final atr over the last period/30 days
        """
        InitialRTAPeriod = 14

        klines = self.client.get_historical_klines(symbol=symbol, interval=interval,
                                              start_str=f"{period + 1} days ago")
        _, closingPrices, highPrices, lowPrices, _, _ = self.utils.format_kline_data(klines=klines)
        InitialTRs, TRs, ATRs = [], [], []

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

        # Calculate the rest of ATRs using wilder`s formula
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
    def get_rsi(self, symbol, days=15, interval="1d"):
        """
        Function for getting RSI of given symbol
        :param symbol: The symbol to get RSI
        :param days: The number of days to get RSI
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: The RSI of the symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{days} days ago")
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
    def get_sma(self, symbol, days, interval="1d"):
        """
        Function for calculating SMA of given symbol in the range of given days
        :param symbol: The symbol for calculating the sma of
        :param days: The number of days for calculations
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: SMA of given symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{days + 1} days ago")
        closePrices = self.crypto.get_closing_prices(klines)
        sma = sum(closePrices) / len(closePrices)
        return sma

    # Function for calculating EMA for given days
    def get_ema(self, symbol, emaDays=14, smaDays=10, timestamp=False, interval="1d"):
        """
        Function for calculating EMA for given days
        :param symbol: The symbol for calculating the ema of
        :param emaDays: The number of days for ema calculations
        :param smaDays: The number of days for calculating the starting SMA
        :param timestamp: Flag for checking if you want to also return corresponding timestamps
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: List of EMAs of given symbol over the span of given days
        """
        # Get the klines
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{emaDays} days ago")
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
    def get_kdj(self, symbol, period, interval="1d"):
        """
        Function for calculating KDJ for given symbol over the given period of time
        :param symbol: Symbol to calculate KDJ of
        :param period: Period of time for calculation
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: KDJ data
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
        _, closePrices, highPrices, lowPrices, closeTimes, _ = self.utils.format_kline_data(klines=klines)
        # Lists for the KDJs
        Ks, Ds, Js = [], [], []

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
    def get_boll(self, symbol, period=14, dictionary=False, interval="1d"):
        """
        Function for calculating bollinger lines for given symbol over given period of time
        :param symbol: symbol for calculating the bollinger of
        :param period: period of time for calculation
        :param dictionary: if true return dictionary with data
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: mb, ub, lb lines
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
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
    def get_avl(self, symbol, period=14, interval="1d"):
        """
        Function for calculating AVL of given symbol over given period of time
        :param symbol: symbol for calculating the AVL of
        :param period: period of time for calculation
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: AVL of given symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval,
                                              start_str=f"{period} days ago")
        # Get the trade volumes
        volumes = self.crypto.get_data_from_klines(klines, "Volume")
        # Calculate AVL
        AVL = sum(volumes) / len(volumes)
        return AVL

    # Function for calculating liquidity for given symbol over given period of time
    def get_liquidity(self, symbol, period=1, dictionary=False, interval="1d"):
        """
        Function for calculating liquidity for given symbol over given period of time
        :param symbol: symbol for calculating the liquidity
        :param period: period of time for calculation
        :param dictionary: if true return dictionary with data
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: liquidity of given symbol
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
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
    def get_cci(self, symbol, period, timestamp=False, interval="1h"):
        """
        Function for getting cci of given symbol
        :param symbol: symbol to calculate cci of
        :param period: period of cci
        :param timestamp: if true returns cci data + timestamp
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: CCI data
        """
        # Get the price data
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
        _, closingPrices, highPrices, lowPrices, timestamps, _ = self.utils.format_kline_data(klines=klines)
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
        # Get the data
        bids = orderData['bids']
        asks = orderData['asks']
        bidAverage = self.crypto.calculate_weighted_average(bids)
        askAverage = self.crypto.calculate_weighted_average(asks)

        spread = bidAverage - askAverage
        if spread < 0:
            spread = 0

        # Return dictionary if needed
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
    def get_volatility(self, symbol, period, average=False, timestamp=False, interval="1h"):
        """
        Function for getting volatility percentage of given symbol over the span of given days
        :param symbol: symbol to calculate volatility of
        :param period: number of days for measuring
        :param average: If true functions returns average volatility
        :param timestamp: If true functions returns volatilities+corresponding timestamps
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :return: list of daily volatilities and timestamps
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, start_str=f"{period} days ago")
        openingPrices, _, highPrices, lowPrices, timestamps, _ = self.utils.format_kline_data(klines=klines)
        # Get the volatility data
        percentageVolatilities = []
        for i in range(len(openingPrices)):
            volatilityPercentage = (highPrices[i] - lowPrices[i]) / openingPrices[i] * 100
            percentageVolatilities.append(volatilityPercentage)
        # Return based on desired data
        if average:
            return sum(percentageVolatilities) / len(percentageVolatilities)

        if timestamp:
            return percentageVolatilities, timestamps

        return percentageVolatilities