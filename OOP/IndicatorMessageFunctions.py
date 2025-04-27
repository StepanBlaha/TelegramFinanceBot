

class IndicatorMessage:
    def __init__(self, Crypto, AI, Utils, Indicators, Plot, Dataframe, Admin):
        self.crypto = Crypto
        self.ai = AI
        self.admin = Admin
        self.utils = Utils
        self.plot = Plot
        self.dataframe = Dataframe
        self.indicators = Indicators

    async def send_cci(self, update, symbol):
        """
        Function for sending a CCI chart photo for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the CCI chart is generated
        :return:
        """
        await update.message.reply_photo(photo=self.plot.plot_cci(symbol), caption=f"CCI chart for {symbol}.")

    async def send_mfi(self, update, symbol):
        """
        Function for sending the MFI value for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the MFI is retrieved
        :return:
        """
        await update.message.reply_text(f"The MFI for {symbol}: {self.indicators.get_mfi(symbol)}.")

    async def send_atr(self, update, symbol):
        """
        Function for sending the ATR value for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the ATR is retrieved
        :return:
        """
        await update.message.reply_text(f"The ATR for {symbol}: {self.indicators.get_atr(symbol)}.")

    async def send_rsi(self, update, symbol, days=14):
        """
        Function for sending the RSI value for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the RSI is retrieved
        :param days: number of days over which RSI is calculated
        :return:
        """
        await update.message.reply_text(f"The RSI for {symbol} for the last {days} days: {self.indicators.get_rsi(symbol)}.")

    async def send_avl(self, update, symbol, days=14):
        """
        Function for sending the AVL value for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the AVL is retrieved
        :param days: number of days over which AVL is calculated
        :return:
        """
        await update.message.reply_text(f"The AVL for {symbol} for the last {days} days: {self.indicators.get_avl(symbol)}.")

    async def send_boll(self, update, symbol):
        """
        Function for sending the Bollinger Bands data for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the Bollinger Bands are retrieved
        :return:
        """
        boll_data = self.indicators.get_boll(symbol, dictionary=True)
        await update.message.reply_text(
            f"The bollinger lines for {symbol}:\n  middle band: {boll_data['MB']}\n  lower band: {boll_data['LB']}\n  upper band: {boll_data['UB']}")

    async def send_ema(self, update, symbol, days=14):
        """
        Function for sending an EMA chart and EMA data for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the EMA is retrieved
        :param days: number of days over which EMA is calculated
        :return:
        """
        await update.message.reply_photo(photo=self.plot.plot_ema(symbol, days), caption=f"EMA chart for {symbol} over {days} days."),
        await update.message.reply_text(f"Here is the EMA data:\n```\n{self.dataframe.get_ema_dataframe(symbol, days)}\n```",
                                        parse_mode="Markdown")

    async def send_kdj(self, update, symbol, days=14):
        """
        Function for sending a KDJ chart and KDJ data for a given symbol
        :param update: update object from Telegram API
        :param symbol: symbol for which the KDJ is retrieved
        :param days: number of days over which KDJ is calculated
        :return:
        """
        await update.message.reply_photo(photo=self.plot.plot_kdj(symbol, days), caption=f"KDJ chart for {symbol} over {days} days.")
        await update.message.reply_text(f"Here is the KDJ data:\n```\n{self.dataframe.get_kdj_dataframe(symbol, days)}\n```",
                                        parse_mode="Markdown")