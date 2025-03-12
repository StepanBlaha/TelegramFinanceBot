from telegram import Bot, BotCommand
import asyncio
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from TelegramBotFunctions import *
from automaticFunctions import digest
from library.utils import *
from mongoFunctions import *
bot = Bot("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU")

functionDict = {
    "digest": digest,
}

records = select("Digest")
for record in records:
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
        print("Not the time to load.")
        continue

    #Get the other values
    interval = record["interval"]
    functionName = record["function"]
    args = record["args"]
    userId = record["userId"]
    recordId = str(record["_id"])
    #Call the function
    functionName(args, userId, bot)
    #Get the last process
    newLastProcess = unix_to_timestamp(nextProcess)
    #Get the new next process
    newNextProcess = seconds_to_unix(interval)
    newNextProcess = unix_to_timestamp(newNextProcess)
    update("Digest", recordId, newLastProcess, newNextProcess)
