from dotenv import load_dotenv
from .models import authConfiguration

import os

# Load the .env file located one folder up
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

settings = authConfiguration(
    server_url=os.getenv("SERVER_URL"),
    realm=os.getenv("REALM"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    authorization_url=os.getenv("AUTHORIZATION_URL"),
    token_url=os.getenv("TOKEN_URL")
)