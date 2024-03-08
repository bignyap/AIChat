''' Authentication Module '''

import uvicorn

# fastapi lib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

# custom modules
from routers.auth import router as auth_router

load_dotenv()

app = FastAPI(
    description="Auth service using Keycloak",
    title="Auth service Application",
    root_path = "/auth_service/v1"
)

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Auth server is running."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)