from bson import ObjectId
from pymongo.synchronous.database import Database
import abc
from mongo import *
class DB:
    def __init__(self, col, query=None, postId =None, values=None):
        self.col = col
        self.db = db_connect()
        self.collection = self.db[col]
        self.query = query
        self.postId = postId
        self.values = values

    def insert(self):
        """
        Function for inserting data into mongo db
        :param col: collection to insert into
        :param query: data to insert
        :return:
        """

        insertedId = self.collection.insert_one(self.query).inserted_id
        print(f'Successfully inserted {insertedId}')

    def select(self):
        """
        Function for selecting data from mongo db
        :param col: collection to select from
        :param query: query to select
        :return: data from mongo db
        """

        DatabaseResponse = []

        if self.query:
            DatabaseResponse = self.collection.find(self.query)
        else:
            for record in self.collection.find():
                DatabaseResponse.append(record)

        return DatabaseResponse

    def update(self):
        """
        Function for updating data into mongo db
        :param col: collection to update into
        :param postId: post id to update
        :param values: values to update
        :return: response
        """

        query = {"_id": ObjectId(self.postId)}
        self.collection.update_one(query, self.values)
        return "Successfully updated"

    def delete(self):
        """
        Function for deleting data from mongo db
        :param col: collection to delete from
        :param query: query to delete
        :return: response
        """
        # Connect to db and delete

        result = self.collection.delete_one(self.query)
        if result.deleted_count > 0:
            return "Successfully deleted"
        else:
            return "Failed"


from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import abc

# Base class with abstract methods for MongoDB operations
class DBBase(abc.ABC):
    def __init__(self, uri=None, db_name="TelegramFinance"):
        """
        Initializes the MongoDB connection.
        """
        if uri is None:
            uri = "mongodb+srv://stepa15b:VIHctgxlrjBB45io@firstcluster.fbyfb.mongodb.net/?retryWrites=true&w=majority&appName=firstCluster"
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        try:
            self.client.admin.command('ping')  # Test connection
            print("Connected to MongoDB successfully!")
            self.db = self.client[db_name]
        except Exception as e:
            print(f"Connection failed: {e}")
            self.db = None

    @abc.abstractmethod
    def execute(self, col, query):
        """ Abstract method to execute database operations """
        pass

    def fetch(self, col, query=None):
        """
        Fetch documents from a collection.
        :param col: Collection name
        :param query: Optional filter query
        :return: List of documents
        """
        try:
            collection = self.db[col]
            data = list(collection.find(query or {}))
            return data
        except Exception as e:
            print(f"Fetch failed: {e}")
            return []


class DBInsert(DBBase):
    def __init__(self):
        super().__init__()

    def execute(self, col, query):
        """
        Inserts a document into a collection.
        :param col: Collection name
        :param data: Data to insert (dict)
        """
        try:
            collection = self.db[col]
            result = collection.insert_one(query)
            print(f'Successfully inserted {result.inserted_id}')
        except Exception as e:
            print(f"Insert failed: {e}")

class DBSelect(DBBase):
    def __init__(self):
        super().__init__()

    def execute(self, col, query=None):
        """
        Retrieves documents from a collection.
        :param col: Collection name
        :param query: Query filter (optional)
        :return: List of documents
        """
        return self.fetch(col, query)

# Class for updating documents
class DBUpdate(DBBase):
    def __init__(self):
        super().__init__()

    def execute(self, col, postId, values):
        """
        Updates a document in a collection.
        :param col: Collection name
        :param postId: Document ID to update
        :param values: Dictionary of updated fields
        """
        try:
            collection = self.db[col]
            result = collection.update_one({"_id": ObjectId(postId)}, {"$set": values})
            if result.matched_count > 0:
                print("Successfully updated document")
                return "Successfully updated"
            else:
                return "No matching document found"
        except Exception as e:
            print(f"Update failed: {e}")
            return "Update failed"


# Class for deleting documents
class DBDelete(DBBase):
    def __init__(self):
        super().__init__()

    def execute(self, col, query):
        """
        Deletes a document from a collection.
        :param col: Collection name
        :param query: Query to delete
        """
        try:
            collection = self.db[col]
            result = collection.delete_one(query)
            if result.deleted_count > 0:
                print("Successfully deleted document")
                return "Successfully deleted"
            else:
                return "No matching document found"
        except Exception as e:
            print(f"Delete failed: {e}")
            return "Delete failed"


# Final class combining all operations for easier use
class MongoDB(DBInsert, DBSelect, DBUpdate, DBDelete):
    def __init__(self):
        super().__init__()

    def close(self):
        """ Closes the MongoDB connection """
        self.client.close()
        print("🔒 Connection closed.")


if __name__ == "__main__":
    db = MongoDB()

    # Insert a new user
    new_id = db.execute("Users", {"name": "John pork", "email": "exa@gmail.com"})

    # Select all users
    print("Users:")
    users = db.execute("Users")
    for user in users:
        print(user)

    # Update user
    if new_id:
        db.execute("Users", postId = new_id, {"email": "skib@gmail.com"})

    # Delete user
    if new_id:
        db.execute("Users", {"_id": ObjectId(new_id)})

    # Close database connection
    db.close()