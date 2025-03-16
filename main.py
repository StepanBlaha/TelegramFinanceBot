

# customizace, moznost nastavit jaky akcie a kryptomeny kdy chci sledovat, v tu dobuy alerty, rozdil cen mezi 2 datumy a jakym smerem
# porovnavani cen aktiv vuci sobe
# alerty pokud zacnou velky zmeny
# v oznameni statistiky posledni doby co si user nastavi
# registrace pomoci telegramu, zaply bot muze byt na pc kdyztak cloud

# jak casto notifikace, jednorazove nebo nekolikrat, po nejaky dobe zrusit upozorneni
# moznost nastavit upozorneni pokud cena vzroste ci klesne o nejaky pocet procent

# nemusi to bezet porad, jen treba v nastavenou dobu, provedou se scany a spocitaji se data
# kazdy den jaky z mych vybranych kryptomen je pod ci nad klouzavym prumerem

# zdroje: yahoo finace, burzy napr. binance,..

# lib python telegrambot

import logging

from telegram import Bot, BotCommand
import asyncio
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from TelegramBotFunctions import *
from ai.chatgptBot import messageChatgpt
from ai.chatgptFunctions import msgChatbot
from ai.geminiBot import messageGemini
from library.utils import *
from mongoFunctions import *
from ai import *
# ------------------------------------Nefunguje--------------------------------------------------------

# ------------------------------------Nefunguje--------------------------------------------------------


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

# __name__ zajisti ze log file se bude jmenovat jako soucasny soubor
logger = logging.getLogger(__name__)

# V update jsous tornuty data o zprave napr i kdo to poslal, to potom beru pres update.effective_user
# Context ma v sobe docasne bot a user data, neco jako session storage
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    user = update.effective_user
    # ceka na message od usera a odpovi v text formatu
    await update.message.reply_text(
        "hello my niuhah",
        # tohle nastavi at vyzaduje odpoved
        reply_markup=ForceReply(selective=True),
    )
async def help(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text("Help")

async def echo(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(update.message.text)



# Function for getting all the bot commands
#------------------------------------Nefunguje--------------------------------------------------------
async def list_commands(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    commands = await context.bot.get_my_commands()
    if commands:
        for command in commands:
            await update.message.reply_text(f"Command: {command.command}, Description: {command.description}")
    else:
        await update.message.reply_text("No commands available.")
#------------------------------------Nefunguje--------------------------------------------------------


# Function for getting base info about symbol
async def symbol_info(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # Takes user given argument
    user_arg = "".join(context.args)
    response = format_symbol_info(user_arg.upper())
    await update.message.reply_text(response)


# Function for returning price chart for desired symbol
async def price_chart(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # Takes user given argument
    try:
        symbol = context.args[0]
        period = int(context.args[1])
        graph = plot_price_in_time(symbol, period)
        await update.message.reply_photo( photo = graph, caption=f"Price chart for {symbol} over {period} days.")
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")


async def kdj(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # Takes user given argument
    try:
        symbol = context.args[0]
        period = int(context.args[1])
        graph = plot_kdj(symbol, period)
        dataframe = get_kdj_dataframe(symbol, period)
        await update.message.reply_photo( photo = graph, caption=f"KDJ chart for {symbol} over {period} days.")
        await update.message.reply_text(f"Here is the KDJ data:\n```\n{dataframe}\n```", parse_mode="Markdown")
        #await update.message.reply_document(document=dataframe, filename="data.csv")
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

async def ema(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # Takes user given argument
    try:
        symbol = context.args[0]
        period = int(context.args[1])
        graph = plot_ema(symbol, period)
        dataframe = get_ema_dataframe(symbol, period)
        await update.message.reply_photo( photo = graph, caption=f"EMA chart for {symbol} over {period} days.")
        await update.message.reply_text(f"Here is the EMA data:\n```\n{dataframe}\n```", parse_mode="Markdown")
        #await update.message.reply_document(document=dataframe, filename="data.csv")
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")



# Example - usefull for future
async def send_msg_to_user( user_chat_id: int, text: str, bot):
    await bot.send_message(chat_id=user_chat_id, text=text)

async def send(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:

    id = update.effective_user.id
    text =f"dsmfsnd {id}"
    await send_msg_to_user( user_chat_id=id, text=text, bot = context.bot)


# format:
# /digest mena interval optional
async def setDigest(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    # dictionary for possible user intervals
    intervalDIct = {
        "daily": 86400,
        "weekly": 604800,
        "monthly": 3072000,
        "yearly": 3652000
    }
    # Takes user given argument
    try:
        func = "digest"
        userId = update.effective_user.id
        symbol = context.args[0]
        interval = context.args[1]
        if interval.isdigit():
            interval = int(interval)
            interval = interval * 3600
        else:
            interval = intervalDIct[interval.lower()]

        # Format the function arguments
        if len(context.args) > 2:
            optionalPeriod = int(context.args[2])
            args = [symbol, optionalPeriod]
        else:
            args = [symbol]

        # Get current last proces
        curUnix = int(time.time())
        curUnix = unix_to_timestamp(curUnix)

        # Get next process
        nextUnix = seconds_to_unix(interval)
        nextUnix = unix_to_timestamp(nextUnix)
        # Get the query and insert data into db
        query = formatInsertQuery(format=func, userId=userId, func=func, interval=interval, lastProcess=curUnix, nextProcess=nextUnix, args=args)
        insert(col="Digest", query=query)
        await update.message.reply_text("Digest settings updated successfully.")

    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

#format
#/set_monitor mena margin
async def priceMonitor(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        func = "priceMonitor"
        userId = update.effective_user.id
        symbol = context.args[0].upper()
        margin = float(context.args[1])
        lastPrice = float(current_price(symbol))
        # Get the query and insert into db
        query = formatInsertQuery(format=func, userId=userId, func=func, margin=margin, lastPrice=lastPrice, symbol=symbol)
        insert(col="Pricemonitor", query=query)
        await update.message.reply_text("Price monitor set successfully.")
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

async def cryptoUpdate(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    intervalDIct = {
        "daily": 86400,
        "weekly": 604800,
        "monthly": 3072000,
        "yearly": 3652000
    }
    try:
        func = "cryptoUpdate"
        userId = update.effective_user.id
        symbol = context.args[0].upper()

        # Format the interval correctly
        interval = context.args[1]
        if interval.isdigit():
            interval = int(interval)
            interval = interval * 3600
        else:
            interval = intervalDIct[interval.lower()]

        # Get current last proces
        lastProcess = int(time.time())
        lastProcess = unix_to_timestamp(lastProcess)

        # Get next process
        nextProcess = seconds_to_unix(interval)
        nextProcess = unix_to_timestamp(nextProcess)

        # Get current price
        lastPrice = float(current_price(symbol))

        query = formatInsertQuery(format="cryptoUpdate", userId=userId, func=func, interval=interval, lastProcess=lastProcess, nextProcess=nextProcess, lastPrice=lastPrice, symbol=symbol)
        insert(col="Userfunctions", query=query)
        await update.message.reply_text("Crypto update settings updated successfully.")
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

#format
#/my_functions funkce
async def showUserFunctions(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        # Get the parameters
        func = context.args[0]
        col = func.lower().capitalize()
        userId = update.effective_user.id
        # Get the formated database response
        response = formatedDatabaseResponse(col, userId=userId, func=func )
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

#format
#/delete funkce symbol val(interval/margin
#interval psany v hodinach
async def deleteFunction(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        #Get all the necessary data
        func = context.args[0]
        col = func.lower().capitalize()
        userId = update.effective_user.id
        symbol = context.args[1]
        val = int(context.args[2])
        # Format the delete query and delete
        query = formatDeleteQuery(userId, func, symbol, val)
        response = delete(col, query)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(str(e))
        await update.message.reply_text("Problem in deleting. Check for any format mistakes.")


#format
#/chatbot message
#interval psany v hodinach
async def chatbot(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        msg = context.args[0]
        response = msgChatbot(msg)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

#format
#/tradeAdvice symbol
async def tradeAdvice(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        symbol = context.args[0]
        functionResponse = trade_advice(symbol, 14)
        aiResponse = get_gpt_trade_advice(symbol)
        await update.message.reply_text(f'Here is your trading advice for {symbol}\n\n Calculated advice: {functionResponse}\n OpenAI advice: {aiResponse}')
    except Exception as e:
        await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

def main():
    # aplication.builder() ja na zakladni build bota .token() ma v sobe nas api key a .buiuld() build provede
    application = Application.builder().token("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU").build()

    # zaregistruje comand (nazev komandu, callback funcke)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("commands", list_commands))
    application.add_handler(CommandHandler("symbol_info", symbol_info))
    application.add_handler(CommandHandler("price_chart", price_chart))
    application.add_handler(CommandHandler("KDJ", kdj))
    application.add_handler(CommandHandler("EMA", ema))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(CommandHandler("digest", setDigest))
    application.add_handler(CommandHandler("set_monitor", priceMonitor))

    application.add_handler(CommandHandler("my_functions", showUserFunctions))
    application.add_handler(CommandHandler("delete", deleteFunction))
    application.add_handler(CommandHandler("chatbot", chatbot))
    application.add_handler(CommandHandler("trade_advice", tradeAdvice))


    # pridam neco na handlovani zprav filter.TEXT jsou vsechny textopve zpravy a filtyer.COMMAND jsou vsechny commandy zacinajici s /
    # kdyz dam pred filter ~ je to jako bych dal v php ! a tedy to neguje
    # tady to zavola echo funcki pokud je zprava text a ne command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # run_polling zacne bota a spusti jeho running loop, nekonecne checkuje(polluje) server a hleda noive zpravy
    # allowed_updates=Update.ALL_TYPES dela ze bot bere vsechno co se stane, fungovalo by to i bez toho ale bot by poslouchal a bral jen zpravy, takhle bere treba i kdyz se nekdo pripoji do roomky
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    chat = messageChatgpt("is bitcon worth investing into")
    print(chat)
    main()