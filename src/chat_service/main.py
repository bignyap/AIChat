'''
Module doc string
'''

# Main Imports
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routers.chat import router as chat_router

from dotenv import load_dotenv

load_dotenv()

# Initialize App
app = FastAPI()

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the routers
app.include_router(chat_router)

# Check Health
@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Chat server is running."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)