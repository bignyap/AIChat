#/config.py
from .models import authConfiguration


settings = authConfiguration(
    server_url="https://localhost:8443/auth/",
    realm="master",
    client_id="llm-fe",
    client_secret="",
    authorization_url="https://localhost/auth/realms/master/protocol/openid-connect/auth",
    token_url="https://localhost/auth/realms/master/protocol/openid-connect/token",
)