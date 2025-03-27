from binance.client import Client
import pandas as np
import time
from datetime import datetime

class Utils:
    def __init__(self):
        pass


    def is_number(self, val):
        """
        Function for checking if given value is a number
        :param val: value to be checked
        :return: boolean
        """
        try:
            float(val)
            return True
        except ValueError:
            return False

    def is_symbol(self, symbol, client):
        """
        Function for checking if given symbol exists
        :param symbol: symbol to be checked
        :param client: client for binance api
        :return: boolean
        """
        try:
            info = client.get_symbol_info(symbol)
            if not info:
                return False
            return True
        except:
            return False

    # Time conversion functions
    def unix_to_date(self, unix, day=False):
        """
        Function that converts unix timestamp to datetime object
        :param unix: Unix timestamp
        :param day: Marker whether to return timestamp containing hours and minutes or not
        :return: datetime object
        """
        unixTime = int(unix)
        if day:
            return datetime.fromtimestamp(unixTime / 1000).strftime('%Y-%d-%m')
        return datetime.fromtimestamp(unixTime / 1000).strftime('%Y-%m-%d %H:%M:%S')

    def datetime_to_unix(datetime):
        """
        Function that converts datetime to unix timestamp
        :param datetime: Datetime to convert
        :return: Unix timestamp
        """
        return int(datetime.timestamp())

    def seconds_to_unix(self, seconds):
        """
        Function that adds seconds to unix timestamp
        :param seconds: Seconds to convert
        :return: Unix timestamp
        """
        return int(time.time()) + seconds

    def unix_to_timestamp(self, unix):
        """
        Function that converts unix timestamp to datetime object
        :param unix: Unix timestamp
        :return: Timestamp object
        """
        timestamp = datetime.fromtimestamp(unix)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def formatedDatabaseResponse(self, col, userId=None, func=None):
        """
        Function that formats database's response into a message
        :param col: Collection to select from
        :param userId: id of user to select
        :param func: function to select
        :return: formated database response
        """
        if func and userId:
            selectQuery = {"userId": userId, "function": func}
            response = select(col=col, query=selectQuery)
            formatedResponse = "Here are your set functions:\n\n"
            format = func.lower()

            for row in response:
                # Format  the response based on db
                if format == "digest":
                    # Format the interval
                    if row["interval"] > 86400:
                        interval = str((row["interval"] / 86400)) + " Days"
                    else:
                        interval = str((row["interval"] / 3600)) + " Hours"
                    # Format the record into a string
                    record = f'Function: {row["function"]}, Symbol: {row["arguments"][0]}, Interval: {interval}'

                elif format == "pricemonitor":
                    record = f'Function: {row["function"]}, Symbol: {row["symbol"]}, Monitor change margin: {row["margin"]}%'

                elif format == "cryptoupdate":
                    # Format the interval
                    if row["interval"] > 86400:
                        interval = str((row["interval"] / 86400)) + " Days"
                    else:
                        interval = str((row["interval"] / 3600)) + " Hours"
                    # Format the record into a string
                    record = f'Function: {row["function"]}, Symbol: {row["symbol"]}, Interval: {interval}'

                else:
                    record = "Invalid database"
                formatedResponse = formatedResponse + record
                formatedResponse = formatedResponse + '\n'
            return formatedResponse
        return "Not enough data"

    # Function that formats database delete query
    def formatDeleteQuery(self, userId, func, symbol, val):
        """
        Function that formats database delete query
        :param userId: id of user
        :param func: function
        :param symbol: symbol
        :param val: value
        :return: formated query string
        """
        if func == "digest":
            val = int(val) * 3600
            query = {
                "userId": userId,
                "function": func,
                "arguments.0": symbol,
                "interval": val
            }

        elif func == "priceMonitor":
            val = int(val)
            query = {
                "userId": userId,
                "function": func,
                "symbol": symbol,
                "margin": val
            }
        elif func == "cryptoUpdate":
            val = int(val) * 3600
            query = {
                "userId": userId,
                "function": func,
                "symbol": symbol,
                "interval": val
            }
        elif func == "balance":
            query = {
                "userId": userId,
                "symbol": symbol,
            }
        else:
            return "Invalid database"
        return query

    # Function for formating db update query
    def formatUpdateQuery(self, format, newPrice=None, lastProcess=None, nextProcess=None, amount=None):
        """
        Function for formating db update query
        :param format: format
        :param newPrice: new price
        :param lastProcess: time of the last process
        :param nextProcess: time of the next process
        :param amount: amount
        :return: formated query string
        """
        formatDict = {
            "digest": {"$set": {"lastProcess": lastProcess, "nextProcess": nextProcess}},
            "priceMonitor": {"$set": {"lastPrice": newPrice}},
            "cryptoUpdate": {"$set": {"lastProcess": lastProcess, "nextProcess": nextProcess, "lastPrice": newPrice}},
            "balance": {"$set": {"amount": amount}},
        }
        query = formatDict[format]
        return query

    # Function for formating db insert query
    def formatInsertQuery(self, format, userId, func=None, lastProcess=None, nextProcess=None, interval=None, symbol=None,
                          margin=None, lastPrice=None, args=None, amount=None):
        """
        Function for formating db insert query
        :param format: format
        :param userId: id of user
        :param func: function
        :param lastProcess: time of the last process
        :param nextProcess: time of the next process
        :param interval: interval between processes
        :param symbol: symbol
        :param margin: margin
        :param lastPrice: last price
        :param args: arguments
        :param amount: amount
        :return: formated query string
        """
        formatDict = {
            "digest":
                {
                    "userId": userId,
                    "function": func,
                    "arguments": args,
                    "interval": interval,
                    "lastProcess": lastProcess,
                    "nextProcess": nextProcess
                },
            "priceMonitor":
                {
                    "userId": userId,
                    "function": func,
                    "symbol": symbol,
                    "margin": margin,
                    "lastPrice": lastPrice
                },
            "cryptoUpdate":
                {
                    "userId": userId,
                    "function": func,
                    "symbol": symbol,
                    "interval": interval,
                    "lastPrice": lastPrice,
                    "lastProcess": lastProcess,
                    "nextProcess": nextProcess
                },
            "balance":
                {
                    "userId": userId,
                    "symbol": symbol,
                    "amount": amount
                },
            "log":
                {
                    "userId": userId,
                    "function": func,
                    "symbol": symbol,
                    "args": args
                },
            "user":
                {
                    "userId": userId,
                    "role": "user"
                }

        }

        try:
            query = formatDict[format]
            return query
        except Exception as e:
            return "Invalid set of arguments"

    # Function for formating the balance response from mongo after running "/balance"
    def formatBalanceResponse(self, data, dictionary=False):
        """
        Function for formating the balance response from mongo after running "/balance"
        :param data: data to format
        :param dictionary: if true returns dictionary with data
        :return: formated data
        """
        formatedResponse = ""
        for i in data:
            formatedStr = f"\n{i['symbol']}: {i['amount']}"
            formatedResponse = formatedResponse + formatedStr

        if dictionary:
            dataDict = {}

            for i in data:
                dataDict[i["symbol"]] = {
                    "symbol": i["symbol"],
                    "amount": i["amount"]
                }

            return dataDict

        return formatedResponse
