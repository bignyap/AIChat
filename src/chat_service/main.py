'''
Module doc string
'''

# Main Imports
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import get_user_info
from auth.models import User

from routers.thread import router as thread_router
from routers.chat import router as chat_router
from routers.speech import router as speech_router

from dotenv import load_dotenv

load_dotenv()

# Initialize App
app = FastAPI(
    description="Chat service using OpenAI and FastAPI",
    title="OpenAPI Chat Application"
)

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Add the routers
# app.include_router(thread_router)
# app.include_router(chat_router)
# app.include_router(speech_router)

# Check Health
@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Chat server is running."


@app.get("/get_user_info")
async def root(user: User = Depends(get_user_info)):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)