''' Authentication Module '''

# core python libraries for handling datetime, etc.
import os
from datetime import datetime, timedelta

# hashing and verify passwords
from passlib.context import CryptContext

# generate and verify jwt token
from jose import JWTError, jwt

# pydantic base model
from pydantic import BaseModel

# Read Env variables
from dotenv import load_dotenv

# for MySQL related operations
import mysql.connector
from mysql.connector import Error

 # take environment variables from .env
load_dotenv(".env")


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

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
    hashed_key: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_key):
    '''Verify plain password with hashed password'''
    return pwd_context.verify(plain_password, hashed_key)


def get_password_hash(password):
    '''Convert password to hashed version'''
    return pwd_context.hash(password)


def get_user(username: str):
    '''Given the username, get the details from database'''
    try:
        with sqlconn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            user_row = cur.fetchone()
            return user_row
    except Error as e:
         # Handle the error or log it
        print(f"Error in getting user details: {e}")
        return None

def authenticate_user(username: str, password: str):
    '''Authenticate the user'''
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_key']):
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
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_jwt_token(encoded_jwt: str):
    
    ''' decode jwt token '''
    
    try:
        decoded = jwt.decode(
            encoded_jwt, JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        return decoded
    except JWTError as exc:
        return exc