# User related CRUD

from typing import Any, Annotated
from fastapi import HTTPException, Depends

from .database import get_db_cursor, insert_data

def store_and_update_user_info(
    cursor: Annotated[Any, Depends(get_db_cursor)],
    user_info: dict
):
    try:
        query = "SELECT * FROM users WHERE uuid = (%s,)"
        cursor.execute(query, (user_info["id"]))
        user_detail = cursor.fetchone()

        if user_detail.length() > 0:
            return user_detail

        query = "INSERT INTO users (uuid, username, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
        values = (
            user_info["id"],
            user_info["username"],
            user_info["email"],
            user_info["first_name"],
            user_info["last_name"]
        )
        user_id = insert_data(cursor=cursor, query=query, values=[values])

        user_detail = user_info
        user_detail["uuid"] = user_info["id"]
        user_detail["id"] = user_id[0][0]
        return user_detail
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while checking user details") from e