"""
Database related operations
"""

import datetime
import random

from typing import List
from fastapi import HTTPException, Depends

from database import get_db_cursor, execute_insertion_stmt, execute_select_stmt, select_data
import model

def is_accessible_thread(user_id: int, thread_id: int, cursor=Depends(get_db_cursor)):
    '''
    Check if the user has access to this particular thread
    '''
    try:
        cursor.execute("SELECT COUNT(*) FROM users_thrads_messages WHERE user_id=%s AND thread_id=%s", (user_id, thread_id))
        count = cursor.fetchone()[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    
    return count > 0


def get_random_system_prompt():
    """
    Randomly choose the prompt from a preselected prompts
    """
    learn_instruction = {
        "role": "system",
        "content":"You are interviewing the user for a job as retail assistant. Ask sort questions that are relevant to the junior assistant to you. Your name is Veronica. The user called Bignya. Keep your answers short below under words"
    }
    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour"
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question"

    return learn_instruction


def get_recent_messages(user_id: int, thread_id: int):
    """
    Get recent messages
    """
    
    # Check if the user has access to the message thread
    is_thread_accessible = is_accessible_thread(user_id, thread_id)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to retrieve the message thread")
    
    # Get the system prompt
    learn_instruction = get_random_system_prompt()

    # Get the messages in the thread
    messages = get_thread_messages(thread_id)

    # Append instruction to message
    messages.append(learn_instruction)

    return messages


def get_thread_messages(thread_id: int):
    """
    Find all the messages in the thread
    """
    sql_stmt = "SELECT messages.id as message_id, messages.message, messages.role, messages.date_created " \
        "FROM users_thrads_messages " \
        "LEFT JOIN messages ON messages.id = users_thrads_messages.message_id " \
        "WHERE users_thrads_messages.thread_id = %s"
    
    messages_data = select_data(sql_stmt, (thread_id,))
    messages = []
    for msg in messages_data:
        message = {
            "message_id": msg['message_id'],
            "message": msg['message'],
            "role": msg['role'],
            "date_created": msg['date_created'].isoformat()
        }
        messages.append(message)
    
    return messages


def store_messages(user_id: int, thread_id: int, request_message: str, response_message: str):
    """
    Store the messages
    """

    # Store the message
    user_message = {"role":"user", "content":request_message}
    assistant_message = {"role":"system", "content":response_message}
    messages = [user_message, assistant_message]
    try:
        message_ids = insert_messages(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to store messages") from e

    # Link the message to its corresponding thread
    thread_messages = []
    for message_id in message_ids:
        thread_messages.append(
            model.UserThreadMessage(user_id=user_id, thread_id=thread_id, message_id=message_id)
        )

    try:
        insert_user_thread_messages(thread_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to link messages to thread") from e


def insert_messages(messages: List[dict]):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO messages(message, date_created, role)"
        "VALUES (%s, %s, %s)"
    ) 
    data = [(message['content'], datetime.datetime.now(), message['role']) for message in messages]
    try:
        message_ids = execute_insertion_stmt(query=insert_stmt, values=data)
    except Exception as e:
        raise e
    
    return message_ids


def insert_user_thread_messages(thread_messages: List[model.UserThreadMessage]):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO users_thrads_messages(user_id, thread_id, message_id)"
        "VALUES (%s, %s, %s)"
    ) 
    data = [(msg.user_id, msg.thread_id, msg.message_id) for msg in thread_messages]

    try:
        execute_insertion_stmt(query=insert_stmt, values=data)
    except Exception as e:
        raise e
    

def delete_thread_message(message_id: int, user_id: int, thread_id: int):
    """
    Delete a message from a thread if the user has access
    """

    # Check if the user has access to the message thread
    is_thread_accessible = is_accessible_thread(user_id, thread_id)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete message from the thread")

    # Delete the message
    delete_stmt = "DELETE FROM users_thrads_messages WHERE message_id = %s AND user_id = %s AND thread_id = %s"
    execute_select_stmt(delete_stmt, values = (message_id, user_id, thread_id))


def delete_all_thread_message(user_id: int, thread_id: int):
    """
    Delete a message from a thread if the user has access
    """

    # Check if the user has access to the message thread
    is_thread_accessible = is_accessible_thread(user_id, thread_id)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete message from the thread")

    # Delete the message
    delete_stmt = "DELETE FROM users_thrads_messages WHERE thread_id = %s"
    execute_select_stmt(delete_stmt, values = (thread_id, ))


def delete_thread(thread_id: int, user_id: int):
    """
    Delete an entire thread if the user has access
    """

    # Check if the user has access to the thread
    is_thread_accessible = is_accessible_thread(user_id, thread_id)
    if not is_thread_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete the thread")

    # Delete all messages associated with the thread
    delete_all_thread_message(user_id, thread_id)

    # Delete the thread
    delete_thread_stmt = "DELETE FROM threads WHERE id = %s"
    execute_select_stmt(delete_thread_stmt, values = (thread_id, ))


