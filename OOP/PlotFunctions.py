from autoload import *


class Plot:
    def __init__(self, Client, Utils, Indicators):
        self.client = Client
        self.utils = Utils
        self.indicators = Indicators

    # Function for generating graph of prices of symbol over specified period
    def plot_price_in_time(self, symbol, period):
        """
        Function for generating graph of prices of symbol over specified period
        :param symbol: Symbol to plot
        :param period: Number of days to plot
        :return:
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=self.client.KLINE_INTERVAL_1HOUR,
                                                   start_str=f"{period} days ago")
        timestamps = []
        closingPrices = []
        for i in range(len(klines)):
            currentKline = klines[i]
            curTime = self.utils.unix_to_date(int(currentKline[6]))
            timestamps.append(curTime)
            closingPrices.append(float(currentKline[4]))

        plt.plot(timestamps, closingPrices)
        # Calculate the timestamp step size
        num_ticks = 10
        step = len(timestamps) // num_ticks
        IoStream = self.utils.format_plot(symbol=symbol, name="Historical Prices", bottom_margin=0.3, left_margin=0.15, ticks=timestamps[::step])
        return IoStream

    # Function for getting graph of EMA for given symbol over period of time
    def plot_ema(self, symbol, period):
        """
        Function for getting graph of EMA for given symbol over period of time
        :param symbol: Symbol to calculate EMA of
        :param period: Period of time for calculation
        :return: Ema graph of given symbol
        """
        # Get the Ema data and corresponding timestamps
        emas, timestamps = self.indicators.get_ema(symbol=symbol, emaDays=period, timestamp=True)
        # Replace the timestamps with unix
        for i in range(len(timestamps)):
            timestamps[i] = self.utils.unix_to_date(int(timestamps[i]), day=True)
        # Plot setup
        plt.plot(timestamps, emas, marker='o')
        IoStream = self.utils.format_plot(symbol=symbol, name="EMA data", bottom_margin=0.3, left_margin=0.15)
        return IoStream

    # Function for getting graph of KDJ for given symbol over period of time
    def plot_kdj(self, symbol, period):
        """
        Function for getting graph of KDJ for given symbol over period of time
        :param symbol: Symbol to calculate KDJ of
        :param period: Period of time for calculation
        :return:
        """
        Ks, Ds, Js, closeTimes = self.indicators.get_kdj(symbol, period)
        plt.plot(closeTimes, Ks, label="K")
        plt.plot(closeTimes, Ds, label="D")
        plt.plot(closeTimes, Js, label="J")
        # Plot setup
        IoStream = self.utils.format_plot(symbol=symbol, name="KDJ data", bottom_margin=0.2, legend_show=True)
        return IoStream

    # Function for plotting volatility graph
    def plot_volatility(self, symbol, period):
        volatilities, timestamps = self.indicators.get_volatility(symbol=symbol, period=period, timestamp=True)
        # Replace the timestamps with unix
        for i in range(len(timestamps)):
            timestamps[i] = self.utils.unix_to_date(int(timestamps[i]))
        # Calculate the timestamp stepsize
        num_ticks = 7
        step = len(timestamps) // num_ticks

        # Get only the decired timestamps
        ticks = []
        ticks.append(timestamps[0])
        ticks.append(timestamps[-1])
        for i in range(step, len(timestamps) - 1, step):
            ticks.append(timestamps[i])

        plt.plot(timestamps, volatilities, marker='o')
        IoStream = self.utils.format_plot(symbol=symbol, name="Volatility data", bottom_margin=0.3, left_margin=0.15, ticks=ticks)
        return IoStream

    # Function for plotting cci graph
    def plot_cci(self, symbol, period=14):
        """
        Function for plotting cci graph
        :param symbol: symbol to plot
        :param period: period of cci
        :return: graph
        """
        CCIs, timestamps = self.indicators.get_cci(symbol, period, timestamp=True)
        # Replace the timestamps with unix
        for i in range(len(timestamps)):
            timestamps[i] = self.utils.unix_to_date(int(timestamps[i]))
        # Calculate the timestamp step size
        num_ticks = 7
        step = len(timestamps) // num_ticks

        # Get only the desired timestamps
        ticks = []
        ticks.append(timestamps[0])
        ticks.append(timestamps[-1])
        for i in range(step, len(timestamps) - 1, step):
            ticks.append(timestamps[i])

        plt.plot(timestamps, CCIs)
        IoStream = self.utils.format_plot(symbol=symbol, name="CCI data", bottom_margin=0.3, left_margin=0.15, ticks=ticks)
        return IoStream