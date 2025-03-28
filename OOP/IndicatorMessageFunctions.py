

from CryptoIndicators import Crypto
from AdminFunctions import Admin
from AiFunctions import AI
from UtilsFunctions import Utils
from DatabaseFunctions import MongoDB
from PlotFunctions import Plot
from DataframeFunctions import Dataframe
from IndicatorFunctions import Indicators

class IndicatorMessage:
    def __init__(self):
        self.crypto = Crypto()
        self.ai = AI()
        self.admin = Admin()
        self.utils = Utils()
        self.plot = Plot()
        self.dataframe = Dataframe()
        self.indicators = Indicators()

    async def send_cci(self, update, symbol):
        await update.message.reply_photo(photo=self.plot.plot_cci(symbol), caption=f"CCI chart for {symbol}.")

    async def send_mfi(self, update, symbol):
        await update.message.reply_text(f"The MFI for {symbol}: {self.indicators.get_mfi(symbol)}.")

    async def send_atr(self, update, symbol):
        await update.message.reply_text(f"The ATR for {symbol}: {self.indicators.get_atr(symbol)}.")

    async def send_rsi(self, update, symbol):
        await update.message.reply_text(f"The RSI for {symbol} for the last 14 days: {self.indicators.get_rsi(symbol)}.")

    async def send_avl(self, update, symbol):
        await update.message.reply_text(f"The AVL for {symbol} for the last 14 days: {self.indicators.get_avl(symbol)}.")

    async def send_boll(self, update, symbol):
        await update.message.reply_text(
            f"The bollinger lines for {symbol}:\n  middle band: {self.indicators.get_boll(symbol, dictionary=True)['MB']}\n  lower band: {self.indicators.get_boll(symbol, dictionary=True)['LB']}\n  upper band: {self.indicators.get_boll(symbol, dictionary=True)['UB']}")

    async def send_ema(self, update, symbol):
        await update.message.reply_photo(photo=self.plot.plot_ema(symbol, 14), caption=f"EMA chart for {symbol} over 14 days."),
        await update.message.reply_text(f"Here is the EMA data:\n```\n{self.dataframe.get_ema_dataframe(symbol, 14)}\n```",
                                        parse_mode="Markdown")

    async def send_kdj(self, update, symbol):
        await update.message.reply_photo(photo=self.plot.plot_kdj(symbol, 14), caption=f"KDJ chart for {symbol} over 14 days.")
        await update.message.reply_text(f"Here is the KDJ data:\n```\n{self.dataframe.get_kdj_dataframe(symbol, 14)}\n```",
                                        parse_mode="Markdown")