"""
Database related operations
"""

import datetime

from typing import List, Any, Annotated
from fastapi import HTTPException, Depends

from . import utils
from . import database as db
from . import thread as th
from . import model


def get_recent_messages(
    user_id: int, thread_id: int,
    cursor = Depends(db.get_db_cursor)
):
    """
    Get recent messages
    """
    
    # Check if the user has access to the message thread
    is_thread_accessible = th.is_accessible_thread(cursor=cursor, user_id=user_id, thread_id=thread_id)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to retrieve the message thread")
    
    # Get the system prompt
    learn_instruction = utils.get_random_system_prompt()

    # Get the messages in the thread
    messages = get_thread_messages(thread_id, cursor=cursor)

    # Append instruction to message
    messages.insert(0, learn_instruction)

    return messages


def get_thread_messages(thread_id: int, cursor = Depends(db.get_db_cursor)):
    """
    Find all the messages in the thread
    """
    sql_stmt = "SELECT messages.id as message_id, messages.message, messages.role, messages.date_created " \
        "FROM thrads_messages " \
        "LEFT JOIN messages ON messages.id = thrads_messages.message_id " \
        "WHERE thrads_messages.thread_id = %s"
    
    messages_data = db.select_data(cursor=cursor, query=sql_stmt, values=(thread_id,))
  
    messages = []
    for msg in messages_data:
        message = {
            "message_id": msg[0],
            "message": msg[1],
            "role": msg[2],
            "date_created": msg[3].isoformat()
        }
        messages.append(message)
    
    return messages


def store_messages(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    thread_id: int, request_message: str, response_message: str
):
    """
    Store the messages
    """

    # Store the message
    user_message = {"role":"user", "content":request_message}
    assistant_message = {"role":"assistant", "content":response_message}
    messages = [user_message, assistant_message]
    
    try:
        message_ids = insert_messages(cursor, messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to store messages") from e
    
    message_ids = [item for sublist in message_ids for item in sublist]

    # Link the message to its corresponding thread
    thread_messages = []
    for message_id in message_ids:
        thread_messages.append(
            model.ThreadMessage(thread_id=thread_id, message_id=message_id)
        )

    try:
        insert_thread_messages(cursor, thread_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to link messages to thread") from e


def insert_messages(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    messages: List[dict]
):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO messages(message, date_created, role)"
        "VALUES (%s, %s, %s)"
    ) 
    data = [(message['content'], datetime.datetime.now(), message['role']) for message in messages]

    message_ids = db.execute_insertion_stmt(cursor, query=insert_stmt, values=data)
    return message_ids


def insert_thread_messages(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    thread_messages: List[model.ThreadMessage]
):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO thrads_messages(thread_id, message_id)"
        "VALUES (%s, %s)"
    ) 
    data = [(msg.thread_id, msg.message_id) for msg in thread_messages]

    try:
        db.execute_insertion_stmt(cursor, query=insert_stmt, values=data)
    except Exception as e:
        raise e
    

def delete_thread_message(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    message_id: int, user_id: int, thread_id: int
):
    """
    Delete a message from a thread if the user has access
    """

    # Check if the user has access to the message thread
    is_thread_accessible = th.is_accessible_thread(user_id, thread_id, cursor=cursor)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete message from the thread")

    # Delete the message
    delete_stmt = "DELETE FROM users_thrads_messages WHERE message_id = %s AND user_id = %s AND thread_id = %s"
    db.execute_select_stmt(cursor, query = delete_stmt, values = (message_id, user_id, thread_id))


