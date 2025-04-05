from autoload import *


class Admin:
    def __init__(self, MongoDB, Utils):
        self.db = MongoDB
        self.utils = Utils
#fixed
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
        symbolDict, functionDict = self.utils.format_admin_digest_data(data=requestHistory, symbolDict=symbolDict, functionDict=functionDict)

        # Get the most used symbol and its count
        mostUsedSymbol, mostUsedSymbolCount = self.utils.get_dict_max(dictionary=symbolDict, key=True)
        # Get the most used symbol and its count
        mostUsedFunction, mostUsedFunctionCount = self.utils.get_dict_max(dictionary=functionDict, key=True)

        # Get the most monitored symbol and function
        monitoredSymbols = list(self.db.select(col="Userfunctions"))
        monitoredSymbolsDict = {}
        monitoredFunctionsDict = {}
        monitoredSymbolsDict, monitoredFunctionsDict = self.utils.format_admin_digest_data(data=monitoredSymbols, symbolDict=monitoredSymbolsDict, functionDict=monitoredFunctionsDict, dataType="monitoredSymbols")

        # Get the most monitored symbol and its count
        mostMonitoredSymbol, mostMonitoredSymbolCount = self.utils.get_dict_max(dictionary=monitoredSymbolsDict, key=True)
        # Get the most monitored symbol and its count
        mostMonitoredFunction, mostMonitoredFunctionCount = self.utils.get_dict_max(dictionary=monitoredFunctionsDict, key=True)

        response = f"Bot digest\n\nTotal users: {userCount}\nAdmins: {adminCount}\nMost used function: {mostUsedFunction} - {mostUsedFunctionCount} times\nMost used symbol: {mostUsedSymbol} - {mostUsedSymbolCount} times\nMost used monitor function: {mostMonitoredFunction} - {mostMonitoredFunctionCount} times\nMost monitored symbol: {mostMonitoredSymbol} - {mostMonitoredSymbolCount} times"
        self.db.close()
        return response

#fixed
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

        functionUsedCount = len(list(self.db.select(col="Requesthistory")))
        monitorSetCount = len(list(self.db.select(col="Userfunctions")))

        avgFuncPerUser = functionUsedCount / userCount
        avgMonitorPerUser = monitorSetCount / userCount

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
            return self.utils.format_admin_user_data(collection="Userfunctions", entriesIndex="monitors", counterIndex="monitorCount")

        response = f"User data:\n\nTotal users: {userCount}\nAdmins: {adminCount}\nNumber of functions used: {functionUsedCount}\nNumber of monitors set: {monitorSetCount}\nAverage amount of functions used per user: {avgFuncPerUser}\nAverage amount of monitors set by user: {avgMonitorPerUser}"
        self.db.close()
        return response
#fixed
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

        # Get the formatted request history and monitor data
        symbolDict, differentSymbolsDict = self.utils.format_admin_symbol_data(data=requestHistory, mainIndex="functionCount", secondaryIndex="monitorCount", entriesList=differentSymbols, dataDict=symbolDict)
        symbolDict, differentSymbolsDict = self.utils.format_admin_symbol_data(data=monitoredSymbols, dataType="monitoredSymbols", mainIndex="monitorCount", secondaryIndex="functionCount", entriesList=differentSymbols, dataDict=symbolDict)

        # Get the most used symbol and its count
        mostUsedSymbol, mostUsedSymbolCount = self.utils.get_2D_dict_max(dictionary=symbolDict, val="functionCount", key=True)
        # Get the most monitored symbol and its count
        mostMonitoredSymbol, mostMonitoredSymbolCount = self.utils.get_2D_dict_max(dictionary=symbolDict, val="monitorCount", key=True)

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
#fixed
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
        functionDict, differentFunctions = self.utils.format_admin_function_data(data=requestHistory, mainIndex="functionCount", secondaryIndex="monitorCount", entriesList=differentFunctions, dataDict=functionDict)
        functionDict, differentFunctions = self.utils.format_admin_function_data(data=monitoredFunctions, mainIndex="monitorCount", secondaryIndex="functionCount", entriesList=differentFunctions, dataDict=functionDict)

        # Get the most used and most used monitor function
        mostUsedFunction, mostUsedFunctionCount = self.utils.get_2D_dict_max(dictionary=functionDict, val="functionCount", key=True)
        mostUsedMonitor, mostUsedMonitorCount = self.utils.get_2D_dict_max(dictionary=functionDict, val="monitorCount", key=True)

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