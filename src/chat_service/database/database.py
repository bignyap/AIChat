"""
Database connection package
"""

import os
from typing import List, Annotated, Any, Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from fastapi import HTTPException, Depends

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
    Establishes a connection to the database.
    '''
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        yield connection
    finally:
        connection.close()


# Dependency to get a database cursor
def get_db_cursor(connection=Depends(get_db_connection), dictionary=False):
    '''
    Provides a cursor to interact with the database.
    '''
    try:
        cursor = connection.cursor(dictionary=dictionary)
        yield cursor
    except Error as error:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(error)}") from error
    finally:
        connection.commit()
        cursor.close()


def execute_select_stmt(cursor: Annotated[Any, Depends(get_db_cursor)], query: str, values: tuple = ()):
    """
    Execute SQL query with values and handle transaction rollback and commit
    """
    try:
        cursor.execute(query, values)
    except Error as e:
        raise e
    
    
def select_data(cursor: Annotated[Any, Depends(get_db_cursor)], query: str, values: tuple = ()):
    """
    Example function for SQL select
    """
    execute_select_stmt(cursor, query, values)
    result = cursor.fetchall()
    return result


def execute_insertion_stmt(
    cursor: Annotated[Any, Depends(get_db_cursor)], 
    query: str, 
    values: List[tuple]
):
    """
    Execute SQL query with values and handle transaction rollback and commit
    """
    try:
        cursor.executemany(query, values)
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_inserted_ids = cursor.fetchall()
        return last_inserted_ids
    except Error as e:
        raise e


def insert_data(
    cursor: Annotated[Any, Depends(get_db_cursor)],
    query: str,
    values: Optional[List[tuple]] = None
):
    """
    Example function for inserting multiple rows and retrieving the generated IDs
    """
    if values is None:
        values = []

    return execute_insertion_stmt(cursor, query, values)
