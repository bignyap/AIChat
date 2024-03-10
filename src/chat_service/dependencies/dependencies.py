
# Access token verifier dependencies
import os
import json
import httpx
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from ssl import SSLContext, CERT_NONE

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
    Validate the token
    """
    validate_url = settings.auth_url
    headers = {"Authorization": f"Bearer {token}"}

    # Create a custom SSL context that doesn't verify certificates
    ssl_context = SSLContext()
    ssl_context.verify_mode = CERT_NONE

    async with httpx.AsyncClient(verify=ssl_context) as client:
        try:
            response = await client.post(validate_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e


        

# Dependency function combining get_user_info and store_or_update_user_info
async def get_user_and_update_info(
    token: str = Security(oauth2_scheme),
    cursor = Depends(get_db_cursor)
):
    '''
    Depency for every request
    '''
    user_detail = await get_user_info(token)

    user_detail = store_or_update_user_info(cursor, user_detail)

    return user_detail, cursor
