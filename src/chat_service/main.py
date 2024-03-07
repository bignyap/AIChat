'''
Module doc string
'''

# Main Imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user import router as user_router
from routers.thread import router as thread_router
from routers.chat import router as chat_router
from routers.speech import router as speech_router

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

# Add the routers
app.include_router(user_router)
app.include_router(thread_router)
app.include_router(chat_router)
app.include_router(speech_router)

# Check Health
@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Chat server is running."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)