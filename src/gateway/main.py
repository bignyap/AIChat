'''
Module doc string
'''

import uvicorn

from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from routers.llm import router as llm_router
from routers.limiter import limiter

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(llm_router)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
def read_root():
    """
        Default end point
    
    """
    return "Server is running."


if __name__ == "__main__":
    uvicorn.run(app, port=3000)
    