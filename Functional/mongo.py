from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def db_connect():
    uri = "mongodb+srv://stepa15b:VIHctgxlrjBB45io@firstcluster.fbyfb.mongodb.net/?retryWrites=true&w=majority&appName=firstCluster"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        # Get the desired database
        mydb = client['TelegramFinance']
        return mydb
    except Exception as e:
        print(e)