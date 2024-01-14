'''
Module doc string
'''

import uvicorn

from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Chat server is running."


if __name__ == "__main__":
    uvicorn.run(app, port=8003)