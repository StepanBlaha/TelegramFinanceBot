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
def digest(params, userId, bot):
    #Get the parameters
    symbol = params[0]
    period = params[1] if len(params) > 1 else 14
    graphEMA = plot_ema(symbol, period)
    dataframeEMA = get_ema_dataframe(symbol, period)
    #Tady poslu uzivateli ten graf a dataframe
    graphKDJ = plot_kdj(symbol, period)
    dataframeKDJ = get_kdj_dataframe(symbol, period)
    # Tady poslu uzivateli ten graf a dataframe
    graphPrice = plot_price_in_time(symbol, period)
    # Tady poslu uzivateli ten graf a dataframe

    bot.send_photo(chat_id=userId, photo=graphEMA)
    bot.send_document(chat_id=userId, document=dataframeEMA.to_csv(index=False))
    bot.send_photo(chat_id=userId, photo=graphKDJ)
    bot.send_document(chat_id=userId, document=dataframeKDJ.to_csv(index=False))
    bot.send_photo(chat_id=userId, photo=graphPrice)