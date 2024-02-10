"""
Database related operations
"""

import json
import random

import model
import datetime

from typing import List

from database import execute_insertion_stmt

import model


def is_accessible_thread(cursor, user_id:int, thread_id: int):
    '''
    Check if the user has access to this particular thread
    '''
    try:
        cursor.execute("SELECT COUNT(*) FROM users_thrads_messages WHERE user_id=%i AND thread_id=%i", (user_id, thread_id))
        count = cursor.fetchone()
    except Exception as e:
        return e
    
    return count > 0


def get_recent_messages(cursor, user_id:int, thread_id: int):
    """
    Get recent messages
    """
    
    is_thread_accessible = is_accessible_thread(cursor, user_id, thread_id):


    # Define the file name and learn instruction
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content":"You are interviewing the user for a job as retail assistant. Ask sort questions that are relevant to the junior assistant to you. Your name is Veronica. The user called Bignya. Keep your answers short below under words"
    }

    # Initialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour"
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question"

    # Append instruction to message
    messages.append(learn_instruction)

    # Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append last 5 data
            if data:
                if len(data):
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)

    return messages


def store_messages(
    user_id: int, thread_id: int, 
    request_message: str, 
    response_message: str
):
    """
    Store the messages
    """

    # Store the message
    user_message = {"role":"user", "content":request_message}
    assistant_message = {"role":"system", "content":response_message}
    messages = [user_message, assistant_message]
    try:
        mesage_ids = insert_messages(messages)
    except Exception as e:
        return e
    
    # Link the message to it's corresponding thread
    thread_messages = []
    for messages, mesage_id in zip(messages, mesage_ids):
        thread_messages.append(
            {
                "message_id": mesage_id,
                "user_id": user_id,
                "thread_id": thread_id
            }
        )

    insert_user_thread_messages(thread_messages)


def insert_messages(cursor, messages: List[dict]):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO messages(message, date_created, role)"
        "VALUES (%s, %s, %s)"
    ) 
    data = [(message['content'], datetime.datetime.now(), message['role']) for message in messages]
    try:
        message_ids = execute_insertion_stmt(query=insert_stmt, values=data, cursor=cursor)
    except Exception  as e:
        return e
    
    return message_ids


def insert_user_thread_messages(cursor, thread_messages: List[model.UserThreadMessage]):
    """
    Insert message to database
    """

    insert_stmt = (
        "INSERT INTO users_thrads_messages(user_id, thread_id, message_id)"
        "VALUES (%s, %s, %s)"
    ) 
    data = [(msg.user_id, msg.thread_id, msg.message_id) for msg in thread_messages]

    try:
        return execute_insertion_stmt(query=insert_stmt, values=data, cursor=cursor)
    except Exception  as e:
        return e
