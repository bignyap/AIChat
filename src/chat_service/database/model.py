"""
Schema Models
"""

import datetime
from pydantic import BaseModel

class User(BaseModel):
    '''Represents User class'''
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool

class Thread(BaseModel):
    '''Represents Thread class'''
    name: str
    date_created: datetime.time = datetime.datetime.now()

class Message(BaseModel):
    '''Represents Message class'''
    message: str
    date_created: datetime.time = datetime.datetime.now()
    role: str


class ThreadMessage(BaseModel):
    '''Represents Thread Message Link'''
    message_id: int
    thread_id: int