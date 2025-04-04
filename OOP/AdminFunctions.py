from autoload import *


class Admin:
    def __init__(self, MongoDB, Utils):
        self.db = MongoDB
        self.utils = Utils

    def admin_digest(self):
        """
        Function for getting basic admin info about the bot
        :return: formatted info
        """
        # Get the number of total users and number of admins
        userCount = len(list(self.db.select(col="Users")))
        adminCount = len(list(self.db.select(col="Users", query={"role": "admin"})))

        # Get the request history
        requestHistory = list(self.db.select(col="Requesthistory"))

        # Get the most used function and symbol
        symbolDict = {}
        functionDict = {}
        for i in requestHistory:
            # Counter for usage of function
            if i["function"] not in functionDict and i["function"] is not None:
                functionDict[i["function"]] = 1
            elif i["function"] is not None:
                functionDict[i["function"]] += 1
            # Counter for usage of symbol
            if i["symbol"] not in symbolDict and i["symbol"] is not None:
                symbolDict[i["symbol"]] = 1
            elif i["symbol"] is not None:
                symbolDict[i["symbol"]] += 1

        # Get the most used symbol and its count
        mostUsedSymbol = max(symbolDict, key=symbolDict.get)
        mostUsedSymbolCount = symbolDict[mostUsedSymbol]
        # Get the most used symbol and its count
        mostUsedFunction = max(functionDict, key=functionDict.get)
        mostUsedFunctionCount = functionDict[mostUsedFunction]

        # Get the most monitored symbol and function
        monitoredSymbols = list(self.db.select(col="Userfunctions"))
        monitoredSymbolsDict = {}
        monitoredFunctionsDict = {}
        for i in monitoredSymbols:
            # Get the symbol
            if i["function"] == "digest":
                symbol = i["arguments"][0]
            else:
                symbol = i["symbol"]
            # Counter for usage of symbol
            if symbol not in monitoredSymbolsDict and symbol is not None:
                monitoredSymbolsDict[symbol] = 1
            elif symbol is not None:
                monitoredSymbolsDict[symbol] += 1
            # Counter for usage of function
            if i["function"] not in monitoredFunctionsDict and i["function"] is not None:
                monitoredFunctionsDict[i["function"]] = 1
            elif i["function"] is not None:
                monitoredFunctionsDict[i["function"]] += 1

        # Get the most monitored symbol and its count
        mostMonitoredSymbol = max(monitoredSymbolsDict, key=monitoredSymbolsDict.get)
        mostMonitoredSymbolCount = monitoredSymbolsDict[mostMonitoredSymbol]
        # Get the most monitored symbol and its count
        mostMonitoredFunction = max(monitoredFunctionsDict, key=monitoredFunctionsDict.get)
        mostMonitoredFunctionCount = monitoredFunctionsDict[mostMonitoredFunction]

        response = f"Bot digest\n\nTotal users: {userCount}\nAdmins: {adminCount}\nMost used function: {mostUsedFunction} - {mostUsedFunctionCount} times\nMost used symbol: {mostUsedSymbol} - {mostUsedSymbolCount} times\nMost used monitor function: {mostMonitoredFunction} - {mostMonitoredFunctionCount} times\nMost monitored symbol: {mostMonitoredSymbol} - {mostMonitoredSymbolCount} times"
        self.db.close()
        return response

    def admin_users(self, IDs=False, funcData=False, monitorData=False):
        """
        Function for getting data about users
        :param IDs: if true returns string and list with all the user ids
        :param funcData: if true returns dictionary with the count of functions user used and what functions he used
        :param monitorData: if true returns dictionary with the count of monitor functions user used and what functions he used
        :return: string with basic data about users
        """
        users = list(self.db.select(col="Users"))
        userCount = len(users)
        adminCount = len(list(self.db.select(col="Users", query={"role": "admin"})))

        avgFuncPerUser = len(list(self.db.select(col="Requesthistory"))) / userCount
        avgMonitorPerUser = len(list(self.db.select(col="Userfunctions"))) / userCount

        functionUsedCount = len(list(self.db.select(col="Requesthistory")))
        monitorSetCount = len(list(self.db.select(col="Userfunctions")))

        if IDs:
            # Get all the user ids
            userIDs = []
            IDsMessage = f""
            for i in users:
                userIDs.append(i["userId"])
                IDsMessage += f"\n{i + 1}: {i['userId']}"
            self.db.close()
            return userIDs, IDsMessage

        if funcData:
            return self.utils.format_admin_user_data(collection="Requesthistory", entriesIndex="functions", counterIndex="functionCount")

        if monitorData:
            data = self.utils.format_admin_user_data(collection="Userfunctions", entriesIndex="monitors", counterIndex="monitorCount")
            return data

        response = f"User data:\n\nTotal users: {userCount}\nAdmins: {adminCount}\nNumber of functions used: {functionUsedCount}\nNumber of monitors set: {monitorSetCount}\nAverage amount of functions used per user: {avgFuncPerUser}\nAverage amount of monitors set by user: {avgMonitorPerUser}"
        self.db.close()
        return response

    def admin_symbols(self, dictionary=False):
        """
        Function for getting data about usage of different bot symbols
        :param dictionary: if true return dictionary with data
        :return: formated string with symbol info
        """
        # Get the data
        requestHistory = list(self.db.select(col="Requesthistory"))
        monitoredSymbols = list(self.db.select(col="Userfunctions"))
        self.db.close()
        # Get the number of uses in functions and monitors for each symbol
        symbolDict = {}
        differentSymbols = []
        for i in requestHistory:
            # Counter for usage of symbol
            if i["symbol"] not in symbolDict and i["symbol"] is not None:
                differentSymbols.append(i["symbol"])
                symbolDict[i["symbol"]] = {}
                symbolDict[i["symbol"]]["monitorCount"] = 0
                symbolDict[i["symbol"]]["functionCount"] = 1
            elif i["symbol"] is not None:
                symbolDict[i["symbol"]]["functionCount"] += 1

        # Get the most monitored symbol and function
        for i in monitoredSymbols:
            # Get the symbol
            if i["function"] == "digest":
                symbol = i["arguments"][0]
            else:
                symbol = i["symbol"]
            # Counter for usage of symbol
            if symbol not in symbolDict and symbol is not None:
                differentSymbols.append(symbol)
                symbolDict[i["symbol"]] = {}
                symbolDict[i["symbol"]]["monitorCount"] = 1
                symbolDict[i["symbol"]]["functionCount"] = 0
            elif symbol is not None:
                symbolDict[i["symbol"]]["monitorCount"] += 1

        # Get the most used symbol and its count
        mostUsedSymbol = max(symbolDict, key=lambda k: symbolDict[k]["functionCount"])
        mostUsedSymbolCount = symbolDict[mostUsedSymbol]["functionCount"]
        # Get the most monitored symbol and its count
        mostMonitoredSymbol = max(symbolDict, key=lambda k: symbolDict[k]["monitorCount"])
        mostMonitoredSymbolCount = symbolDict[mostMonitoredSymbol]["monitorCount"]

        if dictionary:
            data = {
                "mostUsedSymbol": mostUsedSymbol,
                "mostUsedSymbolCount": mostUsedSymbolCount,
                "mostMonitoredSymbol": mostMonitoredSymbol,
                "mostMonitoredSymbolCount": mostMonitoredSymbolCount,
                "symbolData": symbolDict,
                "symbols": differentSymbols
            }
            return data

        response = f"Symbol data\n\nNumber of different symbols used: {len(symbolDict)}\nMost used symbol: {mostUsedSymbol} - {mostUsedSymbolCount} times\nMost monitored symbol: {mostMonitoredSymbol} - {mostMonitoredSymbolCount} times"
        return response

    def admin_functions(self, dictionary=False):
        """
        Function for getting data about usage of different bot functions
        :param dictionary: if true return dictionary with data
        :return: formated string with function info
        """
        # Get the data
        requestHistory = list(self.db.select(col="Requesthistory"))
        monitoredFunctions = list(self.db.select(col="Userfunctions"))
        self.db.close()
        functionDict = {}
        differentFunctions = []

        # Fill the dictionary with the function data
        for i in requestHistory:
            if i["function"] not in functionDict and i["function"] is not None:
                differentFunctions.append(i["function"])
                functionDict[i["function"]] = {}
                functionDict[i["function"]]["monitorCount"] = 0
                functionDict[i["function"]]["functionCount"] = 1
                functionDict[i["function"]]["symbols"] = []
            elif i["function"] is not None:
                functionDict[i["function"]]["functionCount"] += 1

            if i["symbol"] not in functionDict and i["symbol"] is not None:
                functionDict[i["function"]]["symbols"].append(i["symbol"])

        for i in monitoredFunctions:
            if i["function"] not in functionDict and i["function"] is not None:
                differentFunctions.append(i["function"])
                functionDict[i["function"]] = {}
                functionDict[i["function"]]["monitorCount"] = 1
                functionDict[i["function"]]["functionCount"] = 0
                functionDict[i["function"]]["symbols"] = []
            elif i["function"] is not None:
                functionDict[i["function"]]["monitorCount"] += 1

            if i["symbol"] not in functionDict and i["symbol"] is not None:
                functionDict[i["function"]]["symbols"].append(i["symbol"])

        # Get the most used and most used monitor function
        mostUsedFunction = max(functionDict, key=lambda k: functionDict[k]["functionCount"])
        mostUsedFunctionCount = functionDict[mostUsedFunction]["functionCount"]

        mostUsedMonitor = max(functionDict, key=lambda k: functionDict[k]["monitorCount"])
        mostUsedMonitorCount = functionDict[mostUsedMonitor]["monitorCount"]

        # Format the dictionary with data
        if dictionary:
            data = {
                "mostUsedFunction": mostUsedFunction,
                "mostUsedFunctionCount": mostUsedFunctionCount,
                "mostUsedMonitor": mostUsedMonitor,
                "mostUsedMonitorCount": mostUsedMonitorCount,
                "functionData": functionDict,
                "functions": differentFunctions
            }

            return data

        # Format response
        response = f"Function data\n\nNumber of different functions used: {len(differentFunctions)}\nMost used function: {mostUsedFunction} - {mostUsedFunctionCount} times\nMost used monitor function: {mostUsedMonitor} - {mostUsedMonitorCount} times"
        return response

