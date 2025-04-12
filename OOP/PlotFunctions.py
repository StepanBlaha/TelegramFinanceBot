from autoload import *


class Plot:
    def __init__(self, Client, Utils, Indicators):
        self.client = Client
        self.utils = Utils
        self.indicators = Indicators

    # Function for generating graph of prices of symbol over specified period
    def plot_price_in_time(self, symbol, period, interval="1h", tickAmount=10):
        """
        Function for generating graph of prices of symbol over specified period
        :param symbol: Symbol to plot
        :param period: Number of days to plot
        :param interval: Binance-compatible interval string like '1m', '1h', '1d', etc.
        :param tickAmount: Number of ticks to plot
        :return:
        """
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval,
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
        num_ticks = tickAmount
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
    def plot_volatility(self, symbol, period, tickAmount=7):
        """
        Function for getting graph of volatility for given symbol over period of time
        :param symbol: Symbol to calculate volatility of
        :param period: Period of time for calculation
        :param tickAmount: Number of ticks to plot
        :return:
        """
        volatilities, timestamps = self.indicators.get_volatility(symbol=symbol, period=period, timestamp=True)

        # Format the timestamps and ticks
        timestamps, ticks = self.utils.format_plot_timestamps(timestamps=timestamps, tickAmount=tickAmount)

        plt.plot(timestamps, volatilities, marker='o')
        IoStream = self.utils.format_plot(symbol=symbol, name="Volatility data", bottom_margin=0.3, left_margin=0.15, ticks=ticks)
        return IoStream

    # Function for plotting cci graph
    def plot_cci(self, symbol, period=14, tickAmount=7):
        """
        Function for plotting cci graph
        :param symbol: symbol to plot
        :param period: period of cci
        :param tickAmount: Number of ticks to plot
        :return: graph
        """
        CCIs, timestamps = self.indicators.get_cci(symbol, period, timestamp=True)

        # Format the timestamps and ticks
        timestamps, ticks = self.utils.format_plot_timestamps(timestamps=timestamps, tickAmount=tickAmount)

        plt.plot(timestamps, CCIs)
        IoStream = self.utils.format_plot(symbol=symbol, name="CCI data", bottom_margin=0.3, left_margin=0.15, ticks=ticks)
        return IoStream