import psycopg2
from info import *


def create_database():
    # Connect to the default "postgres" database to create a new database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    # Create a new database
    cursor.execute(f"CREATE DATABASE {DB_NAME};")
    # Close the connection to the default database
    cursor.close()
    conn.close()

def create_user():
    # Connect to the newly created database to create a new user
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    # Create a new user
    cursor.execute(f"CREATE USER {DB_USER} WITH ENCRYPTED PASSWORD '{DB_PASSWORD}';")
    # Grant necessary privileges to the user
    cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")
    # Close the connection to the database
    cursor.close()
    conn.close()

def create_table():
    # Connect to the database as the new user to create a new table
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Create a new table
    cursor.execute("""
        CREATE TABLE news (
            timestamp TIMESTAMP,
            title TEXT NOT NULL,
            stock TEXT NOT NULL,
            content JSONB, 
        );
    """)

    # Close the connection to the database
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Create the new database, user, and table
    create_database()
    create_user()
    create_table()