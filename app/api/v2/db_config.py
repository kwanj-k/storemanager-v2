"""
This file contains the database configurations and common operations
"""

#Standard library imports
import os
import psycopg2


config_name = os.getenv('APP_SETTINGS')
development_url = os.getenv('Dev_URL')
testing_url = os.getenv('Test_URL')
try:
    """Put the connection in a try so we know when not connected."""
    if config_name == 'development':
        conn = psycopg2.connect(development_url)
    if config_name == 'testing':
        conn = psycopg2.connect(testing_url)
except:
    print("Database is not connected.")

cur = conn.cursor()

def create_tables():
    """
    This will create all tables defined in tables function
    """
    queries = tables()
    for q in queries:
        cur.execute(q)
    conn.commit()

def drop_all():
    """
    Method to drop all the tables in the database
    """
    cur.execute("DROP TABLE IF EXISTS users CASCADE")
    cur.execute("DROP TABLE IF EXISTS stores CASCADE")
    cur.execute("DROP TABLE IF EXISTS products CASCADE")
    cur.execute("DROP TABLE IF EXISTS carts CASCADE")
    cur.execute("DROP TABLE IF EXISTS sales CASCADE")
    conn.commit()

def tables():
    """
    This function defines the different tables in the database
    It returns all the definitions in a queries list
    """

    stores =  """
        CREATE TABLE IF NOT EXISTS stores(id serial PRIMARY KEY, 
        name varchar, 
        category varchar,
        created_at varchar);
        """

    users = """
        CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, 
        store_id int,
        role int,
        email varchar, 
        password varchar,
        added_at varchar);
        """

    queries = [stores,users]
    return queries