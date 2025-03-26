
from binance.client import Client
import pandas as np
import numpy as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import json
import math

from ai.chatgptFunctions import gptTradeAdvice
from botLoop import functionDict
from library.utils import *
import io
from mongoFunctions import *
from TelegramBotFunctions import *


from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

client = Client()
def admin_digest():
    # Get the number of total users and number of admins
    userCount = len(list(select(col="Users")))
    adminCount = len(list(select(col="Users", query={"role": "admin"})))

    # Get the request history
    requestHistory = list(select(col="Requesthistory"))

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
    monitoredSymbols = list(select(col="Userfunctions"))
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
    return response

def admin_users(IDs=False, funcData=False):
    """
    Function for getting data about users
    :param IDs: if true returns string and list with all the user ids
    :param funcData: if true returns dictionary with the count of functions user used and what functions he used
    :return: string with basic data about users
    """
    users = list(select(col="Users"))
    userCount = len(users)
    adminCount = len(list(select(col="Users", query={"role": "admin"})))
    avgFuncPerUser = len(list(select(col="Requesthistory"))) / userCount
    avgMonitorPerUser = len(list(select(col="Userfunctions"))) / userCount

    if IDs:
        # Get all the user ids
        userIDs=[]
        IDsMessage = f""
        for i in users:
            userIDs.append(i["userId"])
            IDsMessage += f"\n{i+1}: {i['userId']}"

        return userIDs, IDsMessage

    if funcData:
        # Get dictionary with amount of functions user used and what functions he used
        userUsedFuncs = {}
        requestHistory = list(select(col="Requesthistory"))
        for i in requestHistory:
            # Checks if user id is already in the dictionary
            if i["userId"] not in userUsedFuncs and i["userId"] is not None:
                userUsedFuncs[i["userId"]] = {}
                userUsedFuncs[i["userId"]]["functionCount"] = 1
                userUsedFuncs[i["userId"]]["functions"] = []
            elif i["userId"] is not None:
                userUsedFuncs[i["userId"]]["functionCount"] += 1
                if i["function"] not in userUsedFuncs[i["userId"]]["functions"]:
                    userUsedFuncs[i["userId"]]["functions"].append(i["function"])
        return userUsedFuncs

    response = f"User data:\n\nTotal users: {userCount}\nAdmins: {adminCount}\nAverage amount of functions used per user: {avgFuncPerUser}\nAverage amount of monitors set by user: {avgMonitorPerUser}"
    return response

print(admin_users())