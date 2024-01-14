''' Validate access token  for each request through the gateway ''' 
import os

import requests

from fastapi import Request, HTTPException

from dotenv import load_dotenv

DOTEBV_PATH = "../.env"  # Path to the .env file in the parent directory
load_dotenv(DOTEBV_PATH)

AUTH_SVC_ADDRESS = os.environ.get('AUTH_SVC_ADDRESS')
TIMEOUT_LIMIT = 20


async def authorize(request: Request) -> str:
    '''
    Authenticate the User
    This function gets the Authorization header from the request, calls 
    the authenticating service, and return the token if valid.
    '''

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Token missing")

    response = requests.post(
        f"{AUTH_SVC_ADDRESS}/authorize", 
        headers={"Authorization": token},
        timeout = TIMEOUT_LIMIT
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
    
    return token