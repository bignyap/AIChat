# core python libraries for handling datetime, etc.
from datetime import datetime, timedelta
from typing import Annotated
import os

# fastapi lib
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# generate and verify jwt token
from jose import JWTError, jwt

# hashing and verify passwords
from passlib.context import CryptContext

# pydantic base model
from pydantic import BaseModel

# Read Env variables
from dotenv import load_dotenv

# for MySQL related operations
import mysql.connector
from mysql.connector import Error

 # take environment variables from .env
load_dotenv(".env")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

MySQL_HOST = os.getenv("MySQL_HOST")
MySQL_Username = os.getenv("MySQL_Username")
MySQL_Password = os.getenv("MySQL_Password")
MySQL_DB = os.getenv("MySQL_DB")


sqlconn = mysql.connector.connect(
  host = MySQL_HOST,
  user = MySQL_Username,
  password = MySQL_Password,
  database = MySQL_DB
)

class Token(BaseModel):
    '''Represents class with access_token and token_type'''
    access_token: str
    token_type: str

class TokenData(BaseModel):
    '''Represents TokenData class'''
    username: str | None = None


class User(BaseModel):
    '''Represents User class'''
    username: str
    email: str|None = None
    full_name: str|None = None
    disabled: bool|None = None


class UserInDB(User):
    '''Represents UserInDB class'''
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    '''Verify plain password with hashed password'''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    '''Convert password to hashed version'''
    return pwd_context.hash(password)


def get_user(username: str):
    '''Given the username, get the details from database'''
    try:
        with sqlconn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM user WHERE username=%s", (username,))
            user_row = cur.fetchone()
            return user_row
    except Error as e:
         # Handle the error or log it
        print(f"Error in reset_password: {e}")
        return None


def reset_password(username: str, password: str):
    '''Given the username, update the password'''
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    try:
        with sqlconn.cursor(dictionary=True) as cur:
            # Update the password
            hashed_password = get_password_hash(password)
            _ = cur.execute(
                "UPDATE user SET hashed_password = %s WHERE username=%s",
                (hashed_password, username)
            )
        # Commit the changes
        sqlconn.commit()
        return True
    except Error as e:
        # Handle the error or log it
        print(f"Error in reset_password: {e}")
        return False

def authenticate_user(username: str, password: str):
    '''Authenticate the user'''
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    '''Get an access token once anuthenticated'''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    '''Get the currently logged in user'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/register", response_model=TokenData)
async def register_in_app(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    '''Register for the application'''
    uname = form_data.username
    pwd = form_data.password
    reset = reset_password(uname, pwd)
    if not reset:
        raise HTTPException(
            status_code=500, 
            detail="Could not register the user"
        )
    return {"username": uname}

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    '''Access token api'''
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}