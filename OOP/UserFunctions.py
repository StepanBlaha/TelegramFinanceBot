class User:
    def __init__(self, Crypto, Utils, MongoDB):
        self.crypto = Crypto
        self.utils = Utils
        self.db = MongoDB

    # Function for updating the state of users crypto balance in db
    def update_balance(self, symbol, userId, amount, action):
        """
        Function for updating the state of users crypto balance in db
        :param symbol: symbol for choosing which record to update
        :param userId: id of the user
        :param amount: amount for the update
        :param action: action to do
        :return: response
        """
        # Check for invalid action
        if action not in ["remove", "add"]:
            return "Invalid action"

        # Get users data for given symbol
        selectQuery = {"userId": userId, "symbol": symbol}
        selectResponse = list(self.db.select(query=selectQuery, col="Usercrypto"))

        # Check if any record exists
        if len(selectResponse) == 0:
            if action == "remove":
                return "No resources for given symbol"
            else:
                # If the record doesn't exist and the action is "add" create new record
                insertQuery = self.utils.formatInsertQuery(format="balance", func="balance", userId=userId, symbol=symbol, amount=amount)
                insertResponse = self.db.insert(col="Usercrypto", query=insertQuery)
                return "Successfully updated"

        # Get the record data
        currentAmount = selectResponse[0]["amount"]
        recordId = selectResponse[0]["_id"]
        newAmount = 0

        # Get new amount
        if action == "remove":
            if amount > currentAmount:
                return "Invalid amount"
            newAmount = currentAmount - amount
        elif action == "add":
            newAmount = currentAmount + amount

        # Update the record
        updateQuery = self.utils.formatUpdateQuery(format="balance", amount=newAmount)
        updateResponse = self.db.update(col="Usercrypto", postId=recordId, values=updateQuery)
        self.db.close()
        return updateResponse

    # Function for getting users wallet data and their worth
    def get_balance_worth(self, userId, symbol=None, dictionary=None):
        """
        Function for getting users wallet data and their worth
        :param userId: id of user
        :param symbol: optional symbol to look for
        :param dictionary: if true returns dictionary with data
        :return: formatted user wallet data
        """
        if symbol:
            selectQuery = {"userId": userId, "symbol": symbol.upper()}
            response = list(self.db.select(query=selectQuery, col="Usercrypto"))
            if len(response) == 0:
                self.db.close()
                return "No data found for given symbol"
        else:
            selectQuery = {"userId": userId}
            response = list(self.db.select(query=selectQuery, col="Usercrypto"))
            if len(response) == 0:
                self.db.close()
                return "No data found"

        if dictionary:
            responseDict = self.utils.formatBalanceResponse(data=response, dictionary=True)
            for i in responseDict.values():
                currentPrice = self.crypto.current_price(i["symbol"])
                i["value"] = float(currentPrice) * float(i["amount"])
            self.db.close()
            return responseDict

        formatedResponse = ""
        for i in response:
            symbolPrice = self.crypto.current_price(i["symbol"])
            formatedStr = f"Your wallet:\n\nsymbol: {i['symbol']}\namount: {i['amount']}\nvalue: {float(symbolPrice) * float(i['amount'])}"
            formatedResponse = formatedResponse + formatedStr

        self.db.close()
        return formatedResponse

    # Function for registering a new user
    def register_user(self, userId):
        """
        Function for registering a new user
        :param userId: id of the user
        :return:
        """
        # Check if user isn't already registered
        selectQuery = {"userId": userId}
        selectResponse = list(self.db.select(query=selectQuery, col="Users"))

        # If he isn't register him
        if len(selectResponse) == 0:
            insertQuery = self.utils.formatInsertQuery(format="user", userId=userId)
            self.db.insert(col="Users", query=insertQuery)
        self.db.close()
