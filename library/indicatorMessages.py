from Functional.TelegramBotFunctions import *

async def send_cci(update, symbol):
    await update.message.reply_photo(photo=plot_cci(symbol), caption=f"CCI chart for {symbol}.")

async def send_mfi(update, symbol):
    await update.message.reply_text(f"The MFI for {symbol}: {get_mfi(symbol)}.")

async def send_atr(update, symbol):
    await update.message.reply_text(f"The ATR for {symbol}: {get_atr(symbol)}.")


async def send_rsi(update, symbol):
    await update.message.reply_text(f"The RSI for {symbol} for the last 14 days: {get_rsi(symbol)}.")

async def send_avl(update, symbol):
    await update.message.reply_text(f"The AVL for {symbol} for the last 14 days: {get_avl(symbol)}.")

async def send_boll(update, symbol):
    await update.message.reply_text(f"The bollinger lines for {symbol}:\n  middle band: {get_boll(symbol, dictionary=True)['MB']}\n  lower band: {get_boll(symbol, dictionary=True)['LB']}\n  upper band: {get_boll(symbol, dictionary=True)['UB']}")

async def send_ema(update, symbol):
    await update.message.reply_photo(photo=plot_ema(symbol, 14), caption=f"EMA chart for {symbol} over 14 days."),
    await update.message.reply_text(f"Here is the EMA data:\n```\n{get_ema_dataframe(symbol, 14)}\n```", parse_mode = "Markdown")

async def send_kdj(update, symbol):
    await update.message.reply_photo(photo=plot_kdj(symbol, 14), caption=f"KDJ chart for {symbol} over 14 days.")
    await update.message.reply_text(f"Here is the KDJ data:\n```\n{get_kdj_dataframe(symbol, 14)}\n```", parse_mode = "Markdown")