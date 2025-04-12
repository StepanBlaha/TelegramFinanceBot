from autoload import *
class Utils:
    def __init__(self, MongoDB, Crypto):
        self.db = MongoDB
        self.crypto = Crypto

    @staticmethod
    def is_number(val):
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

    @staticmethod
    def is_symbol(symbol, client):
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

    @staticmethod
    def unix_to_date(unix, day=False, time_format='%Y-%m-%d %H:%M:%S', day_time_format='%Y-%d-%m'):
        """
        Function that converts unix timestamp to datetime object
        :param unix: Unix timestamp
        :param day: Marker whether to return timestamp containing hours and minutes or not
        :param time_format: Format of timestamp, default - %Y-%m-%d %H:%M:%S
        :param day_time_format: Format of timestamp for the day option, default - %Y-%d-%m
        :return: datetime object
        """
        unixTime = int(unix)
        if day:
            return datetime.fromtimestamp(unixTime / 1000).strftime(day_time_format)
        return datetime.fromtimestamp(unixTime / 1000).strftime(time_format)

    @staticmethod
    def datetime_to_unix(user_datetime):
        """
        Function that converts datetime to unix timestamp
        :param user_datetime: Datetime to convert
        :return: Unix timestamp
        """
        return int(user_datetime.timestamp())

    @staticmethod
    def seconds_to_unix(seconds):
        """
        Function that adds seconds to unix timestamp
        :param seconds: Seconds to convert
        :return: Unix timestamp
        """
        return int(time.time()) + seconds

    @staticmethod
    def unix_to_timestamp(unix, time_format='%Y-%m-%d %H:%M:%S'):
        """
        Function that converts unix timestamp to datetime object
        :param unix: Unix timestamp
        :param time_format: Format of timestamp, default - %Y-%m-%d %H:%M:%S
        :return: Timestamp object
        """
        timestamp = datetime.fromtimestamp(unix)
        return timestamp.strftime(time_format)

    @staticmethod
    def format_day_hours(seconds):
        """
        Function that formats seconds into days or hours
        :param seconds: number of seconds
        :return: formated time
        """
        if seconds > 86400:
            interval = str((seconds / 86400)) + " Days"
        else:
            interval = str((seconds / 3600)) + " Hours"
        return interval

    @staticmethod
    def get_2D_dict_max(dictionary, val, key=False):
        """
        Function for getting max of desired value from a 2D dictionary
        :param dictionary: dict to get data from
        :param val: data you want to get max of
        :param key: if true returns also the key of the value
        :return: max value
        """
        maxVal = max(dictionary, key=lambda k: dictionary[k][val])
        if key:
            maxKey = dictionary[maxVal][val]
            return maxVal, maxKey
        return maxVal

    @staticmethod
    def get_dict_max(dictionary, key=False):
        """
        Function for getting max of desired value from a dictionary
        :param dictionary: dict to get data from
        :param key: if true returns also the key of the value
        :return: max value
        """
        maxKey = max(dictionary, key=dictionary.get)
        if key:
            maxVal = dictionary[maxKey]
            return maxKey, maxVal
        return maxKey

    @staticmethod
    def formatDeleteQuery(userId, func, symbol, val):
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

    @staticmethod
    def formatUpdateQuery(format, newPrice=None, lastProcess=None, nextProcess=None, amount=None):
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

    @staticmethod
    def formatInsertQuery(format, userId, func=None, lastProcess=None, nextProcess=None, interval=None, symbol=None,
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

    @staticmethod
    def formatBalanceResponse(data, dictionary=False):
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
            response = self.db.select(col=col, query=selectQuery)
            self.db.close()
            formatedResponse = "Here are your set functions:\n\n"
            format = func.lower()

            for row in response:
                # Format  the response based on db
                if format == "digest":
                    # Format the interval
                    interval = self.format_day_hours(row["interval"])
                    # Format the record into a string
                    record = f'Function: {row["function"]}, Symbol: {row["arguments"][0]}, Interval: {interval}'

                elif format == "pricemonitor":
                    record = f'Function: {row["function"]}, Symbol: {row["symbol"]}, Monitor change margin: {row["margin"]}%'

                elif format == "cryptoupdate":
                    # Format the interval
                    interval = self.format_day_hours(row["interval"])
                    # Format the record into a string
                    record = f'Function: {row["function"]}, Symbol: {row["symbol"]}, Interval: {interval}'

                else:
                    record = "Invalid database"
                formatedResponse = formatedResponse + record
                formatedResponse = formatedResponse + '\n'
            return formatedResponse
        return "Not enough data"

    def format_admin_user_data(self, collection, entriesIndex, counterIndex):
        """
        Function for formatting admin user data
        :param collection: collection to select from
        :param entriesIndex: index for different entries in the return dictionary
        :param counterIndex: index for the counter in the return dictionary
        :return: dictionary with admin user data
        """
        # Get dictionary with wanted data
        userData = {}
        dataHistory = list(self.db.select(col=collection))

        for i in dataHistory:
            # Checks if user id is already in the dictionary
            if i["userId"] not in userData and i["userId"] is not None:
                userData[i["userId"]] = {}
                userData[i["userId"]][counterIndex] = 1
                userData[i["userId"]][entriesIndex] = []
                userData[i["userId"]]["symbols"] = []
            elif i["userId"] is not None:
                userData[i["userId"]][counterIndex] += 1

            if i["function"] not in userData[i["userId"]][entriesIndex] and i["function"] is not None:
                userData[i["userId"]][entriesIndex].append(i["function"])

            if i.get("symbol") and i["symbol"] not in userData[i["userId"]]["symbols"]:
                userData[i["userId"]]["symbols"].append(i["symbol"])
        self.db.close()
        return userData

    @staticmethod
    def format_admin_symbol_data(data, mainIndex, secondaryIndex, dataType = None, entriesList = None, dataDict = None):
        """
        Function for formatting admin symbol data
        :param data: data to format
        :param dataType: type of data
        :param entriesList: list of entries
        :param dataDict: dictionary for adding data into
        :param mainIndex: main dictionary index to add to
        :param secondaryIndex: secondary index to instantiate
        :return: dictionary with admin symbol data, list with entries
        """
        if not dataDict:
            dataDict = {}
        if not entriesList:
            entriesList = []

        for i in data:
            if i["function"] == "digest" and dataType == "monitoredSymbols":
                symbol = i["arguments"][0]
            else:
                symbol = i["symbol"]
            # Counter for usage of symbol
            if symbol not in dataDict and symbol is not None:
                entriesList.append(symbol)
                dataDict[symbol] = {}
                dataDict[symbol][secondaryIndex] = 0
                dataDict[symbol][mainIndex] = 1
            elif symbol is not None:
                dataDict[symbol][mainIndex] += 1

        return dataDict, entriesList

    @staticmethod
    def format_admin_function_data(data, mainIndex, secondaryIndex, entriesList = None, dataDict = None):
        """
        Function for formatting admin function data
        :param data: data to format
        :param entriesList: list of entries
        :param dataDict: dictionary for adding data into
        :param mainIndex: main dictionary index to add to
        :param secondaryIndex: secondary index to instantiate
        :return: dictionary with admin function data, list with entries
        """
        if not dataDict:
            dataDict = {}
        if not entriesList:
            entriesList = []

        for i in data:
            if i["function"] not in dataDict and i["function"] is not None:
                entriesList.append(i["function"])
                dataDict[i["function"]] = {}
                dataDict[i["function"]][secondaryIndex] = 0
                dataDict[i["function"]][mainIndex] = 1
                dataDict[i["function"]]["symbols"] = []
            elif i["function"] is not None:
                dataDict[i["function"]][mainIndex] += 1

            if i.get("symbol") and i["symbol"] not in dataDict[i["function"]]["symbols"]:
                dataDict[i["function"]]["symbols"].append(i["symbol"])

        return dataDict, entriesList

    @staticmethod
    def format_admin_digest_data(data, symbolDict=None, functionDict=None, dataType=None):
        """
        Function for formatting admin digest data
        :param data: info to format
        :param symbolDict: dictionary for symbol data
        :param functionDict: dictionary for function data
        :param dataType: optional type of data
        :return: dictionaries with symbol and function data
        """

        if not symbolDict:
            symbolDict = {}
        if not functionDict:
            functionDict = {}

        for i in data:
            # Get the symbol
            if dataType == "monitoredSymbols" and i["function"] == "digest":
                symbol = i["arguments"][0]
            else:
                symbol = i["symbol"]
            # Counter for usage of symbol
            if symbol not in symbolDict and symbol is not None:
                symbolDict[symbol] = 1
            elif symbol is not None:
                symbolDict[symbol] += 1
            # Counter for usage of function
            if i["function"] not in functionDict and i["function"] is not None:
                functionDict[i["function"]] = 1
            elif i["function"] is not None:
                functionDict[i["function"]] += 1

        return symbolDict, functionDict

    @staticmethod
    def format_order_data(data):
        """
        Function for formatting order data
        :param data: list with order data
        :return: average price, average quantity
        """
        averagePrice = 0
        averageQuantity = 0

        for i in range(len(data)):
            averagePrice = averagePrice + float(data[i][0])
            averageQuantity = averageQuantity + float(data[i][1])

        averagePrice = averagePrice / len(data)
        averageQuantity = averageQuantity / len(data)

        return averagePrice, averageQuantity

    @staticmethod
    def format_plot(symbol, name, bottom_margin, left_margin=None, rotation=45, legend_show=False, ticks=None):
        """
        Function to format plot
        :param symbol: symbol for the plot
        :param name: text for the plot title
        :param bottom_margin: margin from bottom
        :param left_margin: margin from left
        :param rotation: rotation angle
        :param legend_show: whether to show legend or not
        :param ticks: labels
        :return: IoStream object
        """
        if ticks:
            plt.xticks(ticks, rotation=rotation, ha="right")
        else:
            plt.xticks(rotation=rotation, ha="right")

        if left_margin:
            plt.subplots_adjust(bottom=bottom_margin, left=left_margin)
        else:
            plt.subplots_adjust(bottom=bottom_margin)
        if legend_show:
            plt.legend()
        plt.title(f"{symbol} {name}")
        IoStream = io.BytesIO()
        plt.savefig(IoStream, format='png')
        IoStream.seek(0)
        plt.close('all')

        return IoStream

    def format_kline_data(self, klines):
        """
        Function for formatting kline data
        :param klines: kline data from api
        :return: openingPrices, closingPrices, highPrices, lowPrices, timestamps, volumes
        """
        openingPrices = self.crypto.get_data_from_klines(klines, "Open price")
        closingPrices = self.crypto.get_data_from_klines(klines, "Close price")
        highPrices = self.crypto.get_data_from_klines(klines, "High price")
        lowPrices = self.crypto.get_data_from_klines(klines, "Low price")
        timestamps = self.crypto.get_data_from_klines(klines, "Close time")
        volumes = self.crypto.get_data_from_klines(klines, "Volume")
        return openingPrices, closingPrices, highPrices, lowPrices, timestamps, volumes

    def format_plot_timestamps(self, timestamps, tickAmount):
        """
        Function for formatting plot timestamps and ticks
        :param timestamps: timestamps to format
        :param tickAmount: amount of ticks
        :return:
        """
        # Replace the timestamps with unix
        for i in range(len(timestamps)):
            timestamps[i] = self.unix_to_date(int(timestamps[i]))
        # Calculate the timestamp step size
        num_ticks = tickAmount
        step = len(timestamps) // num_ticks

        # Get only the desired timestamps
        ticks = []
        ticks.append(timestamps[0])
        ticks.append(timestamps[-1])
        for i in range(step, len(timestamps) - 1, step):
            ticks.append(timestamps[i])

        return timestamps, ticks