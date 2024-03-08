
# Access token verifier dependencies
import os
import json
import httpx
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from config import settings 
from database.database import get_db_cursor
from database.user import store_or_update_user_info

# This is used for fastapi docs authentification
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=os.getenv("AUTHORIZATION_URL"),
    tokenUrl=os.getenv("TOKEN_URL"),
)

async def get_user_info(token: str = Security(oauth2_scheme)) -> dict:
    """
    validate the token
    """
    validate_url = settings.auth_url
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(validate_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content)

    return json.loads(response.content)


# Dependency function combining get_user_info and store_or_update_user_info
async def get_user_and_update_info(
    token: str = Security(oauth2_scheme),
    cursor = Depends(get_db_cursor)
):

    user_detail = await get_user_info(token)

    user_detail = store_or_update_user_info(cursor, user_detail)

    return user_detail, cursor
