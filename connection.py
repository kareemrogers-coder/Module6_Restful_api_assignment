
  ### establishing a connection with the gym database.
    ###database breakdown is located in sql file "workout_db_create"


import mysql.connector # import the mysql connector that we just pip installed

from mysql.connector import Error

def connect_fit():
  

    db_name = 'gym'
    user = 'root'
    password = ''
    host = '127.0.0.1'

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )
        if conn.is_connected():
            print("Connection to sql database successful")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None