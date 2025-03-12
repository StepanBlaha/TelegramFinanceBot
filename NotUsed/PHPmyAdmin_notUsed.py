
import pymysql

import mysql.connector
import pymysql


import mysql.connector
from mysql.connector import Error

connection = None  # Initialize connection to None

try:
    connection = mysql.connector.connect(
        host="a058um.forpsi.com",
        port=3306,
        user="f183912",
        password="U7ncqf97",
        database="f183912",
        connection_timeout=120
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to database!! ", db_Info)
        cursor = connection.cursor()

        # Set global timeout settings (You might want to check if this is needed for your server)
        global_connect_timeout = 'SET GLOBAL connect_timeout=120'
        global_wait_timeout = 'SET GLOBAL wait_timeout=120'
        global_interactive_timeout = 'SET GLOBAL interactive_timeout=120'

        cursor.execute(global_connect_timeout)
        cursor.execute(global_wait_timeout)
        cursor.execute(global_interactive_timeout)

        connection.commit()

except Error as e:
    print("DB connection error:", e)

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Closed connection")
    else:
        print("No active connection to close")