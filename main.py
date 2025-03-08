

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

# ------------------------------------Nefunguje--------------------------------------------------------
bot = Bot("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU")
commands = [
    BotCommand("start", "Start interacting with the bot"),
    BotCommand("help", "Get help on how to use the bot"),
    BotCommand("commands", "Get a list of available commands"),
    BotCommand("symbol_info", "Get the base info about a given symbol. \nFormat: /symbol_info <symbol>"),
    BotCommand("price_chart", "Get a graph of prices of given symbol over the span of given days. \nFormat: /price_chart <symbol> <period>"),
]
#bot.set_my_commands(commands)
bot.set_my_commands([])

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














def main()->None:
    # aplication.builder() ja na zakladni build bota .token() ma v sobe nas api key a .buiuld() build provede
    application = Application.builder().token("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU").build()

    # zaregistruje comand (nazev komandu, callback funcke)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("commands", list_commands))
    application.add_handler(CommandHandler("symbol_info", symbol_info))
    application.add_handler(CommandHandler("price_chart", price_chart))

    # pridam neco na handlovani zprav filter.TEXT jsou vsechny textopve zpravy a filtyer.COMMAND jsou vsechny commandy zacinajici s /
    # kdyz dam pred filter ~ je to jako bych dal v php ! a tedy to neguje
    # tady to zavola echo funcki pokud je zprava text a ne command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # run_polling zacne bota a spusti jeho running loop, nekonecne checkuje(polluje) server a hleda noive zpravy
    # allowed_updates=Update.ALL_TYPES dela ze bot bere vsechno co se stane, fungovalo by to i bez toho ale bot by poslouchal a bral jen zpravy, takhle bere treba i kdyz se nekdo pripoji do roomky
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()