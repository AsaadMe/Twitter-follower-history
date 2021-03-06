import psycopg2
from psycopg2 import OperationalError



def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(connection):
    connection.autocommit = True
    cursor = connection.cursor()
    create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        count INTEGER,
        date TEXT
    )
    """
    try:
        cursor.execute(create_users_table)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def insert_exec(connection, query, values):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query, *par):
    connection.autocommit = True
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, tuple(par))
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")