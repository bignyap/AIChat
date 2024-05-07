"""
Database related operations
"""

import datetime
import uuid
from typing import List, Any, Annotated
from fastapi import HTTPException, Depends
# from . import utils
from . import database as db
from . import thread as th
from . import prompt as dbp


def get_default_model(
    user_id:int, 
    cursor = Depends(db.get_db_cursor)
):
    """
    Get the default chat model to use
    """
    sql_stmt = "SELECT default_model from user_setting WHERE user_id = %s"
    
    return db.select_data(cursor=cursor, query=sql_stmt, values=(user_id,), dictionary=False)


def update_default_model(
    user_id:int, model_name: str,
    cursor = Depends(db.get_db_cursor)
):
    """
    Get the default chat model to use
    """
    sql_stmt = "UPDATE user_setting SET default_model = %s WHERE user_id = %s"
    db.execute_select_stmt(cursor=cursor, query=sql_stmt, values=(model_name, user_id))

    return

def insert_default_model(
    user_id:int, model_name: str,
    cursor = Depends(db.get_db_cursor)
):
    """
    Get the default chat model to use
    """
    sql_stmt = (
        "INSERT INTO user_setting(user_id, default_model)"
        "VALUES (%s, %s)"
    )
    db.execute_insertion_stmt(cursor=cursor, query=sql_stmt, values=[(user_id, model_name,)])

    return


def check_default_model(
    user_id:int,
    cursor = Depends(db.get_db_cursor)
):
    """
    Get the default chat model, if not stor the default value
    """
    model_name = get_default_model(user_id, cursor=cursor)

    if (len(model_name) < 1):
        model_name = "gpt-3.5-turbo"
        insert_default_model(user_id, model_name, cursor=cursor)
    else:
        model_name = model_name[0][0]

    return model_name


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
    try:
        system_prompt = get_thread_prompt(cursor=cursor, thread_id=thread_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get system prompt for the thread") from e

    system_prompt = {
        "role": "system",
        "content":system_prompt
    }
    
    # Get the messages in the thread
    messages = get_thread_messages(thread_id, cursor=cursor)

    # Append instruction to message
    messages.insert(0, system_prompt)

    return messages


def get_thread_prompt(
    thread_id: int, user_id: int,
    cursor=Depends(db.get_db_cursor)
):
    """
    Find all the messages in the thread
    """

    sql_stmt = "SELECT prompt_id, prompt FROM threads WHERE id = %s"
    
    prompt_details = db.select_data(cursor=cursor, query=sql_stmt, values=(thread_id,), dictionary=True)
    prompt_details = prompt_details[0]

    if prompt_details["prompt"] is None and prompt_details["prompt_id"] is None:
        return None
    
    if prompt_details["prompt"] is not None:
        return prompt_details["prompt"]

    if prompt_details["prompt_id"] is None:
        prompt_id = dbp.check_default_prompt(cursor=cursor, user_id=user_id)

    prompt_id = prompt_details["prompt_id"]

    prompt = dbp.get_user_prompt(cursor=cursor, prompt_id=prompt_id)
        
    return prompt[0]["prompt"]


def get_thread_messages(
    thread_id: int,
    cursor=Depends(db.get_db_cursor)
):
    """
    Find all the messages in the thread
    """

    sql_stmt = "SELECT id, message_group, message, role, date_created FROM messages WHERE thread_id = %s "\
    "GROUP BY message_group, id ORDER BY id"
    
    messages_data = db.select_data(cursor=cursor, query=sql_stmt, values=(thread_id,), dictionary=True)
    
    messages = []
    if messages_data:
        for msg in messages_data:
            message = {
                "message_id": msg["id"],
                "message_group": msg["message_group"],
                "message": msg["message"],
                "role": msg["role"],
                "date_created": msg["date_created"].isoformat()
            }
            messages.append(message)
    
    return messages


def store_messages(thread_id, request_message, response_message):
    """
    Store the messages
    """
    with db.MyDBContextManager() as connection:
        
        cursor = connection.cursor()

        # Store the message
        user_message = {"role": "user", "content": request_message}
        assistant_message = {"role": "assistant", "content": response_message}
        messages = [user_message, assistant_message]
        group_uuid = str(uuid.uuid4())

        try:
            message_ids = insert_messages(cursor, thread_id, messages, group_uuid)
        except Exception as e:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Failed to store messages") from e
        finally:
            cursor.close()
        
        connection.commit()
        
        message_ids = [item for sublist in message_ids for item in sublist]

    return message_ids


def insert_messages(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    thread_id: int,
    messages: List[dict],
    group_uuid: str
):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO messages(thread_id, message_group, message, date_created, role)"
        "VALUES (%s, %s, %s, %s, %s)"
    ) 
    data = [(thread_id, group_uuid, message['content'], datetime.datetime.now(), message['role']) for message in messages]
    message_ids = db.execute_insertion_stmt(cursor, query=insert_stmt, values=data)
    
    return message_ids

