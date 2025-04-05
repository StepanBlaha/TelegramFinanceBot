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
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """
        Connects to the MongoDB database.
        :return:
        """
        if self.db is None:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            try:
                self.client.admin.command('ping')
                print("Connected to MongoDB successfully!")
                self.db = self.client[self.db_name]
            except Exception as e:
                print(f"Connection failed: {e}")
                self.db = None
        return self.db

    def fetch(self, col, query=None):
        """
        Fetch documents from a collection.
        :param col: Collection name
        :param query: Optional filter query
        :return: List of documents
        """
        try:
            db = self.connect()
            collection = db[col]
            data = list(collection.find(query or {}))
            return data
        except Exception as e:
            print(f"Fetch failed: {e}")
            return []

# Class for inserting documents
class DBInsert(DBBase):
    def __init__(self):
        super().__init__()

    def insert(self, col, query):
        """
        Inserts a document into a collection.
        :param col: Collection name
        :param data: Data to insert (dict)
        """
        db = self.connect()
        try:
            collection = db[col]
            result = collection.insert_one(query)
            print(f'Successfully inserted {result.inserted_id}')
        except Exception as e:
            print(f"Insert failed: {e}")

# Class for selecting documents
class DBSelect(DBBase):
    def __init__(self):
        super().__init__()

    def select(self, col, query=None):
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

    def update(self, col, postId, values):
        """
        Updates a document in a collection.
        :param col: Collection name
        :param postId: Document ID to update
        :param values: Dictionary of updated fields
        """
        db = self.connect()
        try:
            collection = db[col]
            result = collection.update_one({"_id": ObjectId(postId)}, values)
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

    def delete(self, col, query):
        """
        Deletes a document from a collection.
        :param col: Collection name
        :param query: Query to delete
        """
        db = self.connect()
        try:
            collection = db[col]
            result = collection.delete_one(query)
            if result.deleted_count > 0:
                print("Successfully deleted document")
                return "Successfully deleted"
            else:
                return "No matching document found"
        except Exception as e:
            print(f"Delete failed: {e}")
            return "Delete failed"

# Final class combining all operations
class MongoDB(DBInsert, DBSelect, DBUpdate, DBDelete):
    def __init__(self):
        super().__init__()

    def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            print("Connection closed.")