'''
Module doc string
'''

import os
import requests

from fastapi import FastAPI, Request, UploadFile, HTTPException

from company_name import company_name
from pdf_summarizer import pdf_summarizer

AUTH_SVC_ADDRESS = os.getenv("AUTH_SVC_ADDRESS")
TIMEOUT_LIMIT = int(os.getenv("TIMEOUT_LIMIT"))

app = FastAPI()

async def authenticate(request: Request) -> str:
    '''
    Authenticate the User
    This function gets the Authorization header from the request, calls 
    the authenticating service, and return the token if valid.
    '''

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: Token missing")

    response = requests.post(
        f"{AUTH_SVC_ADDRESS}/validate", 
        headers={"Authorization": token},
        timeout = TIMEOUT_LIMIT
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
    
    return token

@app.post("/summarize")
async def llm_summarize(request: Request, file: UploadFile) -> str:
    """
    Endpoint to summarize a PDF file.
    
    """

    try:
        _ = await authenticate(request)

        filepath = await pdf_summarizer.pdf_reader(file)
        res = pdf_summarizer.pdf_summarizer(filepath)

        return res
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.get("/getCompanyName")
async def llm_name(request: Request, product: str, howmany:int = 1) -> str:
    """
    Endpoint to get company names based on product query.
    The number of results is set to 1 by default and can be changed by setting the 'howmany' parameter.
    """

    try:
        _ = await authenticate(request)

        res = company_name.llm_company_name(product, howmany)
        return res
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
