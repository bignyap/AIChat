''' Authentication Module '''

import uvicorn

# fastapi lib
from fastapi import FastAPI
from dotenv import load_dotenv

# custom modules
from routers.auth import router as auth_router

load_dotenv()

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Auth server is running."


if __name__ == "__main__":
    uvicorn.run(app, port=8001)