from telegram import Bot, BotCommand
import asyncio
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from TelegramBotFunctions import *
from automaticFunctions import *
from library.utils import *
import asyncio
from mongoFunctions import *
bot = Bot("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU")

functionDict = {
    "digest": digest,
    "priceMonitor":priceMonitor
}
#Musim z main loopu udelat async funkci a vsechny funkce jako digest taky, kvuli tomu ze bez toho bot. nefunguje
#asyncio.run(func) dela to ze zpusti func v asynchronim rezimu
async def main():
    while True:
        digestRecords = select("Digest")
        for record in digestRecords:
            #Get current unix time
            curTime = int(time.time())
            #Get the next process time
            nextProcess = record["nextProcess"]
            # convert to date object
            nextProcess = datetime.strptime(nextProcess, '%Y-%m-%d %H:%M:%S')
            # convert to unix
            nextProcess = datetime_to_unix(nextProcess)
            # If the next process time is more than 60 seconds later than now continue next cycle iteration
            if nextProcess - curTime > 60:
                continue
            #Get the other values
            interval = record["interval"]
            functionName = record["function"]
            args = record["arguments"]
            userId = record["userId"]
            recordId = str(record["_id"])
            #Call the function
            await functionDict[functionName](args, userId, bot)
            #Get the last process
            newLastProcess = unix_to_timestamp(nextProcess)
            #Get the new next process
            newNextProcess = seconds_to_unix(interval)
            newNextProcess = unix_to_timestamp(newNextProcess)
            #old update func
            #updateDigest("Digest", recordId, newLastProcess, newNextProcess)
            # Get the update query
            query = formatUpdateQuery("digest", lastProcess=newLastProcess, nextProcess=newNextProcess)
            # Update
            update("Digest", recordId, query)
            print(f'Function {functionName} for user {userId} executed successfully.')

        priceMonitorRecords = select("Pricemonitor")
        for record in priceMonitorRecords:
            userId = record["userId"]
            recordId = str(record["_id"])
            functionName = record["function"]
            margin = record["margin"]
            lastPrice = float(record["lastPrice"])
            symbol = record["symbol"]
            print(symbol)
            #calculate one percent of old price
            onePercent = lastPrice / 100
            # calculate margin price from margin percentage
            marginPrice = onePercent * margin
            # Get current price
            curPrice = float(current_price(symbol))

            #Get price difference
            priceDifference = curPrice - lastPrice
            percentageDifference = priceDifference / onePercent
            # check if price is within margin of change
            if(abs(priceDifference) < marginPrice):
                continue

            formatedArguments = [symbol,priceDifference, percentageDifference, lastPrice]
            await functionDict[functionName](formatedArguments, userId, bot)
            # Old update func
            #updatePriceMonitor("priceMonitor", recordId, curPrice)
            # Get the update query
            query = formatUpdateQuery("priceMonitor", newPrice=curPrice)
            # Update
            update("Pricemonitor", recordId, query)


        await asyncio.sleep(10)
if __name__ == "__main__":
    asyncio.run(main())