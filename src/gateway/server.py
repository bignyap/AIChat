'''
Module doc string
'''
from fastapi import FastAPI, Request, UploadFile, HTTPException

from authorize import authorize
from company_name import company_name
from pdf_summarizer import pdf_summarizer

app = FastAPI()

@app.post("/summarize")
async def llm_summarize(request: Request, file: UploadFile) -> str:
    """
    Endpoint to summarize a PDF file.
    
    """

    try:
        _ = await authorize(request)

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
        _ = await authorize(request)

        res = company_name.llm_company_name(product, howmany)
        return res
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
