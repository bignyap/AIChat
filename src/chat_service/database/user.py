# User related CRUD

from typing import Any, Annotated
from fastapi import HTTPException, Depends

from .database import get_db_cursor, insert_data, select_data
from .prompt import check_default_prompt
from .message import check_default_model


def store_or_update_user_info(
    cursor: Annotated[Any, Depends(get_db_cursor)],
    user_info: dict
):
    '''
    Return if the user already exists or store if not
    '''
    
    try:
        query = "SELECT * FROM users WHERE uuid = %s"
        values = (user_info["id"],)
        user_detail = select_data(cursor = cursor, query = query, values = values, dictionary = True)

        if user_detail:
            user_detail =  user_detail[0]
        else:
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

        default_prompt_details = check_default_prompt(cursor=cursor, user_id=user_detail["id"])
        user_detail["default_prompt"] = default_prompt_details["prompt"]
        user_detail["default_prompt_id"] = default_prompt_details["id"]
        user_detail["default_prompt_name"] = default_prompt_details["name"]
        user_detail["default_model"] = check_default_model(cursor=cursor, user_id=user_detail["id"])

        return user_detail
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error while checking user details") from e