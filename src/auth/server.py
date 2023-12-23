''' Authentication Module '''

import os
from datetime import timedelta
from typing import Annotated

# fastapi lib
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# pydantic base model
from pydantic import BaseModel

from jose import JWTError

from authenticate import authenticate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class Token(BaseModel):
    '''Represents class with access_token and token_type'''
    access_token: str
    token_type: str

app = FastAPI()

@app.post("/authorize")
async def validate(
    req: Request
):
    '''Validate access token'''
    encoded_jwt = req.headers["Authorization"]

    if not encoded_jwt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing credentials"
        )

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded_jwt = authenticate.decode_jwt_token(encoded_jwt)
        return decoded_jwt
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        ) from exc


@app.post("/authenticate", response_model=Token)
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    '''Access token api'''
    user = authenticate.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = authenticate.create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}