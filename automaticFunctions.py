from TelegramBotFunctions import *

#1. user nastavi o jake mene chce digest a jak casto, p additionaly bude moct nastavit napr jak moc dozadu data budou
# pr format /digest (<mena>, optional<perioda mereni>) <perioda> (daily, weekly, monthlt, pokud da cislo bere to v hodinach)


from telegram import Bot
bot = Bot("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU")
#while True:
   # condition checkovani z databaze
       # function(params,userid,bot)
    #ex. digest(("BTCUSDT", 9), 623326, bot)

# digest(("BTCUSDT", 9), 623326)


#Funkc ktera bude posilat digest o zmene cen atd specifickemu uzivateli jednou za cas co si sam nastavi
async def digest(params, userId, bot):
    #Get the parameters
    symbol = params[0]
    period = params[1] if len(params) > 1 else 14
    if period == False:
        period = 14

    # Get the base info
    recentPrice = float(current_price(symbol))
    recentTradeVolume = get_recent_traded_volume(symbol, period)
    recentTradeNumber = get_number_of_recent_trades(symbol, period)
    recentTrend = get_recent_trend(symbol, period)
    await bot.send_message(chat_id=userId, text=f"The latest price for {symbol} is: {recentPrice}.\n The traded volume in the last {period} days: {recentTradeVolume}.\n The number of trades made in the last {period} days: {recentTradeNumber}.\n Latest trend: {recentTrend}")

    # Get the price data
    graphPrice = plot_price_in_time(symbol, period)
    await bot.send_photo(chat_id=userId, photo=graphPrice)

    #Get the EMA data
    graphEMA = plot_ema(symbol, period)
    dataframeEMA = get_ema_dataframe(symbol, period)

    await bot.send_photo(chat_id=userId, photo=graphEMA)
    await bot.send_message(chat_id=userId, text=f"Here is the EMA data:\n```\n{dataframeEMA}\n```", parse_mode="Markdown")

    #Get the KDJ data
    graphKDJ = plot_kdj(symbol, period)
    dataframeKDJ = get_kdj_dataframe(symbol, period)

    await bot.send_photo(chat_id=userId, photo=graphKDJ)
    await bot.send_message(chat_id=userId, text=f"Here is the KDJ data:\n```\n{dataframeKDJ}\n```", parse_mode="Markdown")


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

    await bot.send_message(chat_id=userId, text=f" ''''''''''''''''''''''''''''Watch out''''''''''''''''''''''''''''\n\nThe price for {symbol} has changed by {percentageDiff}%\n Old price: {lastPrice}\n New price: {newPrice}\n Price change: {priceDiff}")