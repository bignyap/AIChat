"""
Prompt related operations
"""

from typing import Any, Annotated
from fastapi import HTTPException, Depends

from . import database as db


def is_accessible_prompt(user_id: int, prompt_id: int, cursor=Depends(db.get_db_cursor)):
    '''
    Check if the user has access to this particular prompt
    '''
    try:
        cursor.execute("SELECT COUNT(*) FROM user_prompt WHERE user_id=%s AND id=%s", (user_id, prompt_id))
        count = cursor.fetchone()[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error") from e
    
    return count > 0


def create_prompt(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    prompt_name: str,
    user_id: int,
    prompt: str
):
    """
    Create a new prompt
    """

    # Insert the new prompt into the database
    insert_prompt_stmt = "INSERT INTO user_prompt (user_id, name, prompt) VALUES (%s, %s, %s)"
    prompt_ids = db.insert_data(cursor=cursor, query=insert_prompt_stmt, values=[(user_id, prompt_name, prompt)])

    return prompt_ids[0][0]


def list_prompt(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    user_id: int
):
    """
    List all thread for the user
    """
    select_stmt = "SELECT * FROM user_prompt WHERE user_id=%s"
    prompts = db.select_data(cursor=cursor, query=select_stmt, values=(user_id,), dictionary=True)
    return prompts


def delete_prompt(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    prompt_id: int, user_id: int
):
    """
    Delete an entire thread if the user has access
    """

    # Check if the user has access to the thread
    is_prompt_accessible = is_accessible_prompt(user_id, prompt_id, cursor=cursor)
    if not is_prompt_accessible:
        raise HTTPException(status_code=400, detail="Not able to delete the prompt")

    # Delete the thread
    delete_thread_stmt = "DELETE FROM user_prompt WHERE id = %s"
    db.execute_select_stmt(cursor, delete_thread_stmt, values = (prompt_id, ))


def update_prompt(
    cursor: Annotated[Any, Depends(db.get_db_cursor)],
    prompt_id: int, user_id: int,
    prompt: str
):
    """
    Update an existing thread if the user has access
    """

    # Check if the user has access to the prompt
    is_prompt_accessible = is_accessible_prompt(user_id, prompt_id, cursor=cursor)
    if not is_prompt_accessible:
        raise HTTPException(status_code=403, detail="Not able to update the thread")

    update_prompt_statement = "UPDATE user_prompt SET prompt = %s WHERE id = %s;"

    # Update the thread
    db.execute_select_stmt(cursor, update_prompt_statement, values=tuple([prompt, prompt_id]))