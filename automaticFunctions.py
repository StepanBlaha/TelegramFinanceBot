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

async def cryptoUpdate(symbol, userId, bot, lastPrice, interval):
    # rozdil ceny normalne a procentualne, done
    # tradenuto volume done
    # volatilitu done
    #bid-ask spread done
    # order book imbalance
    #

    currentPrice = float(current_price(symbol))
    priceChange = currentPrice - lastPrice
    percentualChange = (currentPrice - lastPrice) / lastPrice * 100
    await bot.send_message(chat_id=userId, text=f"The latest price for {symbol} is: {currentPrice}.\n Last recorded price: {lastPrice}\n Raw price change: {priceChange}.\n Percentual price change: {percentualChange}%")

    # Get the recent trade data and format them
    tradeData = get_recent_trade_info(symbol=symbol, limit=200, dictionary=True)
    await bot.send_message(chat_id=userId, text=f"Data about recent trades\n\n Total trade volume: {tradeData["tradeVolume"]}\n Total trade price: {tradeData["priceVolume"]}\n Max trade price: {tradeData['maxTradePrice']}\n Min trade price: {tradeData['minTradePrice']}\n Max trade volume: {tradeData["maxTradeQuantity"]}\n Min trade volume: {tradeData["minTradeQuantity"]}\n Average trade price: {tradeData['averageTradePrice']}\n Average trade volume: {tradeData['averageTradeQuantity']}")


    # Format the period for volatility into days
    period = interval/86400
    if period < 1:
        period = 1
    avgPercentVolatility = get_volatility(symbol=symbol, period=period, average=True)
    await bot.send_message(chat_id=userId, text=f"The average percentage volatility: {avgPercentVolatility}%")
    # Get the volatility graph and send it to user
    graphVolatilities = plot_volatility(symbol, period)
    await bot.send_photo(chat_id=userId, photo=graphVolatilities)

    bidAskSpreadData = get_bid_ask_spread(symbol=symbol, dictionary=True)
    await bot.send_message(chat_id=userId, text=f"The average bid-ask spread: {bidAskSpreadData["spread"]}\n Average bid price: {bidAskSpreadData['averageBid']}\n Average ask price: {bidAskSpreadData['averageAsk']}")


    pass
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