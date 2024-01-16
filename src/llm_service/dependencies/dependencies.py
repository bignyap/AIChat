"""
Access token verifier dependencies
"""
import os
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
import httpx

security = HTTPBearer()

async def validate_token(token: str) -> bool:
    """
    validate the token
    """
    validate_url = os.getenv("AUTH_SVC_ADDRESS")
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(validate_url, headers=headers)

    if response.status_code == 200:
        return response.content
    return False


# x_token: Annotated[str, Header()]

async def validate_token_header(
   authorization: str = Depends(security)
):
    """
    get_token_header
    """
    x_token = authorization.credentials
    if not x_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing credentials"
        )

    if not await validate_token(x_token):
        raise HTTPException(status_code=401, detail="Token validation failed")
