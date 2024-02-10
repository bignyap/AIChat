"""
Database connection package
"""

import os

from typing import Optional, List

from fastapi import Depends

import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv

load_dotenv(".env")

# Database configuration
DATABASE_CONFIG = {
    'user': os.getenv("MySQL_Username"),
    'password': os.getenv("MySQL_Password"),
    'host': os.getenv("MySQL_HOST"),
    'database': os.getenv("MySQL_DB"),
    'raise_on_warnings': True
}

# Dependency to get a database connection
def get_db_connection():
    '''
    DB Connector
    '''
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        yield connection
    finally:
        connection.close()


# Dependency to get a database cursor
def get_db_cursor(connection=Depends(get_db_connection)):
    '''
    DB Cursor
    '''
    try:
        cursor = connection.cursor(dictionary=True)
        yield cursor
    finally:
        cursor.close()


def execute_select_stmt(query: str, values: tuple = (), cursor=Depends(get_db_cursor)):
    """
    Execute SQL query with values and handle transaction rollback and commit
    """
    try:
        cursor.execute(query, values)
        cursor.connection.commit()
    except Error as e:
        cursor.connection.rollback()
        raise e
    
    
def select_data(query: str, cursor=Depends(get_db_cursor)):
    """
    Example function for SQL select
    """
    execute_select_stmt(query=query, cursor=cursor)
    result = cursor.fetchall()
    return result


def execute_insertion_stmt(query: str, values: List[tuple], cursor=Depends(get_db_cursor)):
    """
    Execute SQL query with values and handle transaction rollback and commit
    """
    try:
        cursor.executemany(query, values)
        cursor.connection.commit()

        # Retrieve the last inserted IDs
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_inserted_ids = cursor.fetchall()

        return last_inserted_ids
    except Error as e:
        cursor.connection.rollback()
        raise e


def insert_data(query: str, values: Optional[list] = None, cursor=Depends(get_db_cursor)):
    """
    Example function for inserting multiple rows and retrieving the generated IDs
    """
    if values is None:
        values = []

    return execute_insertion_stmt(query=query, values=values, cursor=cursor)
