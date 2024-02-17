"""
Database related operations
"""

import datetime

from typing import Any, Annotated
from fastapi import HTTPException, Depends

from . import database as db


def is_accessible_thread(user_id: int, thread_id: int, cursor=Depends(db.get_db_cursor)):
    '''
    Check if the user has access to this particular thread
    '''
    try:
        cursor.execute("SELECT COUNT(*) FROM threads WHERE creator_id=%s AND id=%s", (user_id, thread_id))
        count = cursor.fetchone()[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    
    return count > 0


def create_thread(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    thread_name: str,
    user_id: int
):
    """
    Create a new thread
    """

    # Insert the new thread into the database
    insert_thread_stmt = "INSERT INTO threads (name, creator_id, date_created) VALUES (%s, %s, %s)"
    current_datetime = datetime.datetime.now()
    thread_ids = db.insert_data(cursor=cursor, query=insert_thread_stmt, values=[(thread_name, user_id, current_datetime)])

    return thread_ids[0][0]


def list_thread(
    cursor: Annotated[Any, Depends(db.get_db_cursor(dictionary=True))],  
    user_id: int
):
    """
    List all thread for the user
    """
    select_stmt = "SELECT * FROM threads WHERE creator_id=%s"
    threads = db.select_data(cursor=cursor, query=select_stmt, values=(user_id,))
    
    return threads


def delete_thread(
    cursor: Annotated[Any, Depends(db.get_db_cursor(dictionary=False))], 
    thread_id: int, user_id: int
):
    """
    Delete an entire thread if the user has access
    """

    # Check if the user has access to the thread
    is_thread_accessible = is_accessible_thread(user_id, thread_id, cursor=cursor)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete the thread")

    # Delete all messages associated with the thread
    delete_all_thread_message(cursor, user_id, thread_id)

    # Delete the thread
    delete_thread_stmt = "DELETE FROM threads WHERE id = %s"
    db.execute_select_stmt(cursor, delete_thread_stmt, values = (thread_id, ))


def delete_all_thread_message(
    cursor: Annotated[Any, Depends(db.get_db_cursor)], 
    user_id: int, thread_id: int
):
    """
    Delete a message from a thread if the user has access
    """

    # Check if the user has access to the message thread
    is_thread_accessible = is_accessible_thread(user_id, thread_id, cursor=cursor)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete message from the thread")

    # Delete the message
    delete_stmt = "DELETE FROM users_thrads_messages WHERE thread_id = %s"
    db.execute_select_stmt(cursor, delete_stmt, values = (thread_id, ))



