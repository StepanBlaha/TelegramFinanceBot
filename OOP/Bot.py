import logging

from telegram import Bot, BotCommand
import asyncio
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import time

from binance.client import Client






from CryptoFunctions import Crypto
from AdminFunctions import Admin
from AiFunctions import AI
from UtilsFunctions import Utils
from DatabaseFunctions import MongoDB
from PlotFunctions import Plot
from DataframeFunctions import Dataframe
from IndicatorMessageFunctions import IndicatorMessage
from IndicatorFunctions import Indicators
from UserFunctions import User

from DependencyContainer import DependencyContainer

class SBBot:
    def __init__(self):
        self.application = Application.builder().token("7493091157:AAEB1e9BKnQtb81QhL-Lcu5X08mXWHvgOjU").build()
        self.add_handlers()

        objects = self.create_objects()
        self.client = objects["client"]
        self.crypto = objects["crypto"]
        self.ai = objects["ai"]
        self.admin = objects["admin"]
        self.utils = objects["utils"]
        self.plot = objects["plot"]
        self.dataframe = objects["dataframe"]
        self.indicator_msg = objects["indicator_message"]
        self.indicators = objects["indicators"]
        self.user = objects["user"]
        self.mongo = objects["mongo"]

    def add_handlers(self):
        """
        Function to add handlers
        :return:
        """
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("commands", self.list_commands))
        self.application.add_handler(CommandHandler("symbol_info", self.symbol_info))
        self.application.add_handler(CommandHandler("price_chart", self.price_chart))
        self.application.add_handler(CommandHandler("KDJ", self.kdj))
        self.application.add_handler(CommandHandler("EMA", self.ema))
        self.application.add_handler(CommandHandler("send", self.send))
        self.application.add_handler(CommandHandler("digest", self.setDigest))
        self.application.add_handler(CommandHandler("set_monitor", self.priceMonitor))

        self.application.add_handler(CommandHandler("my_functions", self.showUserFunctions))
        self.application.add_handler(CommandHandler("delete", self.deleteFunction))
        self.application.add_handler(CommandHandler("chatbot", self.chatbot))
        self.application.add_handler(CommandHandler("trade_advice", self.tradeAdvice))
        self.application.add_handler(CommandHandler("crypto_update", self.cryptoUpdate))

        self.application.add_handler(CommandHandler("indicators", self.indicators_func))
        self.application.add_handler(CommandHandler("balance", self.balance))
        self.application.add_handler(CommandHandler("admin", self.admin_func))

        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

    def create_objects(self):
        """
        Function to create the objects
        :return: dictionary with created objects
        """
        mongo = MongoDB()
        ai = AI()
        admin = Admin(mongo)
        utils = Utils(mongo)
        client = Client()
        # Crypto je none, prida se potom
        indicators = Indicators(client, None, utils)
        dataframe = Dataframe(client, utils, indicators)
        plot = Plot(client, utils, indicators)
        crypto = Crypto(client, ai, utils, indicators, plot, dataframe)
        user = User(crypto, utils, mongo)
        #nevadi mi setovat crypto u indicatoru az potom
        # kdyz predam necemu objekt v pythonu nevytvari kopii ale jakoby dam access k tomu pr.
        # indicators.crypto.status = active tak crypto.status bude taky active
        indicators.crypto = crypto

        indicator_message = IndicatorMessage(crypto, ai, utils, indicators, plot, dataframe, admin)

        return {
            "ai": ai,
            "admin": admin,
            "utils": utils,
            "client": client,
            "indicators": indicators,
            "dataframe": dataframe,
            "plot": plot,
            "crypto": crypto,
            "indicator_message": indicator_message,
            "user": user,
            "mongo": mongo,
        }

    def run(self):
        """
        Run the bot
        :return:
        """
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        print("Bot closing..")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        userId = update.effective_user.id
        # ceka na message od usera a odpovi v text formatu
        await update.message.reply_text(
            "Hello, im SBbot, your personal crypto assistant",
            # tohle nastavi at vyzaduje odpoved
            reply_markup=ForceReply(selective=True),
        )
        self.user.register_user(userId=userId)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        userId = update.effective_user.id
        await update.message.reply_text("Help")

        logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="help")
        self.mongo.insert(col="Requesthistory", query=logQuery)
        self.mongo.close()

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        userId = update.effective_user.id
        await update.message.reply_text(update.message.text)

        logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="echo")
        self.mongo.insert(col="Requesthistory", query=logQuery)
        self.mongo.close()

    # Function for getting all the bot commands
    # ------------------------------------Nefunguje--------------------------------------------------------
    async def list_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        commands = await context.bot.get_my_commands()
        if commands:
            for command in commands:
                await update.message.reply_text(f"Command: {command.command}, Description: {command.description}")
        else:
            await update.message.reply_text("No commands available.")

    # ------------------------------------Nefunguje--------------------------------------------------------

    # Function for getting base info about symbol
    async def symbol_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Takes user given argument
        userId = update.effective_user.id
        user_arg = "".join(context.args)
        response = self.crypto.format_symbol_info(user_arg.upper())

        await update.message.reply_text(response)

        logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=user_arg, func="symbol_info")
        self.mongo.insert(col="Requesthistory", query=logQuery)
        self.mongo.close()

    # Function for returning price chart for desired symbol
    async def price_chart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Takes user given argument
        try:
            userId = update.effective_user.id
            symbol = context.args[0]
            period = int(context.args[1])
            graph = self.plot.plot_price_in_time(symbol, period)

            await update.message.reply_photo(photo=graph, caption=f"Price chart for {symbol} over {period} days.")

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="price_chart",
                                         args=[period])

            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    async def kdj(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Takes user given argument
        try:
            userId = update.effective_user.id
            symbol = context.args[0]
            period = int(context.args[1])
            graph = self.plot.plot_kdj(symbol, period)
            dataframe = self.dataframe.get_kdj_dataframe(symbol, period)

            await update.message.reply_photo(photo=graph, caption=f"KDJ chart for {symbol} over {period} days.")
            await update.message.reply_text(f"Here is the KDJ data:\n```\n{dataframe}\n```", parse_mode="Markdown")

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="kdj", args=[period])

            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
            # await update.message.reply_document(document=dataframe, filename="data.csv")
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    async def ema(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Takes user given argument
        try:
            userId = update.effective_user.id
            symbol = context.args[0].upper()
            period = int(context.args[1])
            graph = self.plot.plot_ema(symbol, period)
            dataframe = self.dataframe.get_ema_dataframe(symbol, period)

            await update.message.reply_photo(photo=graph, caption=f"EMA chart for {symbol} over {period} days.")
            await update.message.reply_text(f"Here is the EMA data:\n```\n{dataframe}\n```", parse_mode="Markdown")

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="ema", args=[period])

            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
            # await update.message.reply_document(document=dataframe, filename="data.csv")
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # format:
    # /indicators symbol <indicator-optional>
    async def indicators_func(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            userId = update.effective_user.id
            symbol = context.args[0]

            if len(context.args) > 1:
                indicator = context.args[1].lower()
                # Dictionary with different functions
                indicatorDict = {
                    "cci": self.indicator_msg.send_cci,
                    "mfi": self.indicator_msg.send_mfi,
                    "atr": self.indicator_msg.send_atr,
                    "rsi": self.indicator_msg.send_rsi,
                    "avl": self.indicator_msg.send_avl,
                    "boll": self.indicator_msg.send_boll,
                    "ema": self.indicator_msg.send_ema,
                    "kdj": self.indicator_msg.send_kdj,
                }

                # Trigger the correct function according to user picked indicator
                await indicatorDict.get(indicator, lambda update, symbol: update.message.reply_text("Invalid indicator."))(update, symbol)

                logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="indicators",
                                             args=[indicator])

                self.mongo.insert(col="Requesthistory", query=logQuery)
                self.mongo.close()

            else:
                # Simple indicator data
                await update.message.reply_text(
                    f"Technical indicators for {symbol}\n\n The MFI for {symbol}: {self.indicators.get_mfi(symbol)}\n The ATR for {symbol}: {self.indicators.get_atr(symbol)}\n The RSI for {symbol} for the last 14 days: {self.indicators.get_rsi(symbol)}\n The AVL for {symbol} for the last 14 days: {self.indicators.get_avl(symbol)}\n The bollinger lines for {symbol}:\n  middle band: {self.indicators.get_boll(symbol, dictionary=True)['MB']}\n  lower band: {self.indicators.get_boll(symbol, dictionary=True)['LB']}\n  upper band: {self.indicators.get_boll(symbol, dictionary=True)['UB']}")
                # EMA data
                await update.message.reply_photo(photo=self.plot.plot_ema(symbol, 14),
                                                 caption=f"EMA chart for {symbol} over 14 days."),
                await update.message.reply_text(f"Here is the EMA data:\n```\n{self.dataframe.get_ema_dataframe(symbol, 14)}\n```",
                                                parse_mode="Markdown")
                # KDJ data
                await update.message.reply_photo(photo=self.plot.plot_kdj(symbol, 14),
                                                 caption=f"KDJ chart for {symbol} over 14 days."),
                await update.message.reply_text(f"Here is the KDJ data:\n```\n{self.dataframe.get_kdj_dataframe(symbol, 14)}\n```",
                                                parse_mode="Markdown")
                # CCI data
                await update.message.reply_photo(photo=self.plot.plot_cci(symbol), caption=f"CCI chart for{symbol}.")

                logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="indicators")

                self.mongo.insert(col="Requesthistory", query=logQuery)
                self.mongo.close()
        except Exception as e:
            await update.message.reply_text(str(e))
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # Example - usefull for future
    async def send_msg_to_user(self, user_chat_id: int, text: str, bot):
        await bot.send_message(chat_id=user_chat_id, text=text)

    async def send(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        id = update.effective_user.id
        text = f"dsmfsnd {id}"
        await self.send_msg_to_user(user_chat_id=id, text=text, bot=context.bot)

        logQuery = self.utils.formatInsertQuery(format="log", userId=id, func="send")
        self.mongo.insert(col="Requesthistory", query=logQuery)
        self.mongo.close()

    # format:
    # /digest mena interval optional
    async def setDigest(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
            curUnix = self.utils.unix_to_timestamp(curUnix)

            # Get next process
            nextUnix = self.utils.seconds_to_unix(interval)
            nextUnix = self.utils.unix_to_timestamp(nextUnix)
            # Get the query and insert data into db

            query = self.utils.formatInsertQuery(format=func, userId=userId, func=func, interval=interval, lastProcess=curUnix,
                                      nextProcess=nextUnix, args=args)
            self.mongo.insert(col="Userfunctions", query=query)

            await update.message.reply_text("Digest settings updated successfully.")

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="Digest",
                                         args={"interval": interval, "currentTimestamp": curUnix})
            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()

        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # format
    # /set_monitor mena margin
    async def priceMonitor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            func = "priceMonitor"
            userId = update.effective_user.id
            symbol = context.args[0].upper()
            margin = float(context.args[1])
            lastPrice = float(self.crypto.current_price(symbol))
            # Get the query and insert into db

            query = self.utils.formatInsertQuery(format=func, userId=userId, func=func, margin=margin, lastPrice=lastPrice,
                                      symbol=symbol)
            self.mongo.insert(col="Userfunctions", query=query)

            await update.message.reply_text("Price monitor set successfully.")

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="priceMonitor",
                                         args={"margin": margin, "lastPrice": lastPrice})
            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # format
    # /crypto_update symbol interval
    async def cryptoUpdate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
            lastProcess = self.utils.unix_to_timestamp(lastProcess)

            # Get next process
            nextProcess = self.utils.seconds_to_unix(interval)
            nextProcess = self.utils.unix_to_timestamp(nextProcess)

            # Get current price
            lastPrice = float(self.crypto.current_price(symbol))


            query = self.utils.formatInsertQuery(format="cryptoUpdate", userId=userId, func=func, interval=interval,
                                      lastProcess=lastProcess, nextProcess=nextProcess, lastPrice=lastPrice,
                                      symbol=symbol)
            self.mongo.insert(col="Userfunctions", query=query)

            await update.message.reply_text("Crypto update settings updated successfully.")

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, symbol=symbol, func="cryptoUpdate",
                                         args={"interval": interval, "currentTimestamp": lastProcess,
                                               "lastPrice": lastPrice})
            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # format
    # /my_functions funkce
    async def showUserFunctions(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            # Get the parameters
            func = context.args[0]
            col = "Userfunctions"
            userId = update.effective_user.id
            # Get the formated database response

            response = self.utils.formatedDatabaseResponse(col, userId=userId, func=func)

            await update.message.reply_text(response)

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="showUserFunctions",
                                         args={"function": func})
            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # format
    # /delete funkce symbol val(interval/margin)
    # interval psany v hodinach
    async def deleteFunction(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            # Get all the necessary data
            func = context.args[0]
            col = "Userfunctions"
            userId = update.effective_user.id
            symbol = context.args[1]
            val = int(context.args[2])
            # Format the delete query and delete

            query = self.utils.formatDeleteQuery(userId, func, symbol, val)
            response = self.mongo.delete(col, query)

            await update.message.reply_text(response)

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="deleteFunction",
                                         args={"symbol": symbol, "value": val, "function": func})
            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()

        except Exception as e:
            await update.message.reply_text(str(e))
            await update.message.reply_text("Problem in deleting. Check for any format mistakes.")

    # format
    # /chatbot message
    # interval psany v hodinach
    async def chatbot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            userId = update.effective_user.id
            msg = context.args[0]
            response = self.ai.msgChatbot(msg)

            await update.message.reply_text(response)

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="chatbot", args={"message": msg})

            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # format
    # /tradeAdvice symbol
    async def tradeAdvice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            userId = update.effective_user.id
            symbol = context.args[0]
            functionResponse = self.crypto.trade_advice(symbol, 14)
            aiResponse = self.crypto.get_gpt_trade_advice(symbol)

            await update.message.reply_text(
                f'Here is your trading advice for {symbol}\n\n Calculated advice: {functionResponse}\n OpenAI advice: {aiResponse}')

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="tradeAdvice", symbol=symbol)

            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    # /balance action symbol amount
    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            actionDict = {
                "show": "show",
                "add": "add",
                "remove": "remove",
                "value": "value"
            }
            # Get the data
            userId = update.effective_user.id
            action = context.args[0].lower()
            symbol = False
            amount = False

            # Error handling
            if action not in actionDict:
                await update.message.reply_text("Please choose an action: show, remove, add.")
                return

            # Get the symbol
            if len(context.args) > 1:
                symbol = context.args[1].upper()

            # Error handling
            if (not symbol and action == "add") or (not symbol and action == "remove"):
                await update.message.reply_text("Add and remove actions require symbol")
                return

            # Different actions

            if action == "show":
                # Get the response based on if symbol is set or not
                if symbol:
                    query = {"userId": userId, "symbol": symbol}
                    response = list(self.mongo.select(query=query, col="Usercrypto"))
                    # Turn the response to readable format
                    response = self.utils.formatBalanceResponse(response)
                else:
                    query = {"userId": userId}
                    response = list(self.mongo.select(query=query, col="Usercrypto"))
                    # Turn the response to readable format
                    response = self.utils.formatBalanceResponse(response)
                await update.message.reply_text(f'Here is your account balance:\n\n {response}')
            elif action == "remove":
                # Error handling
                if not len(context.args) > 2:
                    await update.message.reply_text("This action requires an amount")
                    self.mongo.close()
                    return
                # Get the amount
                amount = context.args[2]
                # Error handling
                if not self.utils.is_number(amount):
                    await update.message.reply_text("Please enter a number")
                    self.mongo.close()
                    return
                # Return the response
                response = self.user.update_balance(symbol=symbol, userId=userId, amount=float(amount), action=action)
                await update.message.reply_text(f'{response} account balance for symbol {symbol}')
            elif action == "add":
                # Error handling
                if not len(context.args) > 2:
                    await update.message.reply_text("This action requires an amount")
                    self.mongo.close()
                    return
                # Get the amount
                amount = context.args[2]
                # Error handling
                if not self.utils.is_number(amount):
                    await update.message.reply_text("Please enter a number")
                    self.mongo.close()
                    return
                # Return the response
                response = self.user.update_balance(symbol=symbol, userId=userId, amount=float(amount), action=action)
                await update.message.reply_text(f'{response} account balance for symbol {symbol}')
            elif action == "value":
                response = self.user.get_balance_worth(userId=userId, symbol=symbol)
                await update.message.reply_text(f'{response}')

            logQuery = self.utils.formatInsertQuery(format="log", userId=userId, func="balance", symbol=symbol,
                                         args={"amount": amount})

            self.mongo.insert(col="Requesthistory", query=logQuery)
            self.mongo.close()
        except Exception as e:
            await update.message.reply_text(str(e))
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")

    async def admin_func(self,  update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            actionDict = {
                "digest": self.admin.admin_digest,
                "users": self.admin.admin_users,
                "symbols": self.admin.admin_symbols,
                "functions": self.admin.admin_functions,
            }
            userId = update.effective_user.id

            # Checks if user picked valid action
            if len(context.args) < 1 or context.args[0].lower() not in actionDict:
                await update.message.reply_text("Please choose a valid action: digest, users, symbols, functions.")
                return

            # Gets the user action
            action = context.args[0].lower()

            # Check if user has admin role

            selectQuery = {"userId": userId}
            selectResponse = list(self.mongo.select(query=selectQuery, col="Users"))
            self.mongo.close()

            if selectResponse[0]["role"] != "admin":
                await update.message.reply_text("You need an admin role to use this command.")
                return

            # Get the data
            response = actionDict[action]()
            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text("Problem in getting response. Check for any format mistakes.")



if __name__ == "__main__":
    bot = SBBot()
    bot.run()