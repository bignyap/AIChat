from dotenv import load_dotenv
import os
from pydantic import BaseModel

class AuthConfiguration(BaseModel):
    mysql_host: str
    mysql_username: str
    mysql_password: str
    mysql_db: str
    authorization_url: str
    token_url: str
    openai_api_key: str
    auth_url: str

def load_missing_env_variables():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    missing_env_vars = []
    
    # Check each environment variable and load missing ones from .env file
    for env_var in ["MySQL_HOST", "MySQL_Username", "MySQL_Password", "MySQL_DB",
                    "AUTHORIZATION_URL", "TOKEN_URL", "OPENAI_API_KEY", "AUTH_SVC_ADDRESS"]:
        if not os.getenv(env_var):
            missing_env_vars.append(env_var)
    
    # Load missing environment variables from .env file
    if missing_env_vars:
        load_dotenv(dotenv_path, override=False)

def get_env_value(env_var_name):
    return os.getenv(env_var_name)

load_missing_env_variables()

settings = AuthConfiguration(
    mysql_host=get_env_value("MySQL_HOST"),
    mysql_username=get_env_value("MySQL_Username"),
    mysql_password=get_env_value("MySQL_Password"),
    mysql_db=get_env_value("MySQL_DB"),
    authorization_url=get_env_value("AUTHORIZATION_URL"),
    token_url=get_env_value("TOKEN_URL"),
    openai_api_key=get_env_value("OPENAI_API_KEY"),
    auth_url=get_env_value("AUTH_SVC_ADDRESS")
)
