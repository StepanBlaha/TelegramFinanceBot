

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

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters









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

def main()->None:
    # aplication.builder() ja na zakladni build bota .token() ma v sobe nas api key a .buiuld() build provede
    application = Application.builder().token("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU").build()

    # zaregistruje comand (nazev komandu, callback funcke)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # pridam neco na handlovani zprav filter.TEXT jsou vsechny textopve zpravy a filtyer.COMMAND jsou vsechny commandy zacinajici s /
    # kdyz dam pred filter ~ je to jako bych dal v php ! a tedy to neguje
    # tady to zavola echo funcki pokud je zprava text a ne command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # run_polling zacne bota a spusti jeho running loop, nekonecne checkuje(polluje) server a hleda noive zpravy
    # allowed_updates=Update.ALL_TYPES dela ze bot bere vsechno co se stane, fungovalo by to i bez toho ale bot by poslouchal a bral jen zpravy, takhle bere treba i kdyz se nekdo pripoji do roomky
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()