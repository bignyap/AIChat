from dotenv import load_dotenv
from auth.models import authConfiguration
import os

def load_missing_env_variables():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    missing_env_vars = []
    
    # Check each environment variable and load missing ones from .env file
    for env_var in ["SERVER_URL", "REALM", "CLIENT_ID", "CLIENT_SECRET",
                    "AUTHORIZATION_URL", "TOKEN_URL"]:
        if not os.getenv(env_var):
            missing_env_vars.append(env_var)
    
    # Load missing environment variables from .env file
    if missing_env_vars:
        load_dotenv(dotenv_path, override=False)

def get_env_value(env_var_name):
    return os.getenv(env_var_name)

load_missing_env_variables()

settings = authConfiguration(
    server_url=os.getenv("SERVER_URL"),
    realm=os.getenv("REALM"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    authorization_url=os.getenv("AUTHORIZATION_URL"),
    token_url=os.getenv("TOKEN_URL")
)
