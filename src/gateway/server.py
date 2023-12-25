'''
Module doc string
'''
from fastapi import FastAPI, UploadFile
# Request, UploadFile, HTTPException

from fastapi.responses import StreamingResponse

# from i_authorize import authorize
from company_name import company_name
from pdf_summarizer import pdf_summarizer

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/summarize")
async def llm_summarize(file: UploadFile) -> str:
    """
    Endpoint to summarize a PDF file.
    
    """
    filepath = pdf_summarizer.pdf_reader(file)
    res = pdf_summarizer.pdf_summarizer(filepath)

    return res


@app.get("/getCompanyName")
async def company_name_stream(product: str, howmany:int = 1) -> str:
    """
    Endpoint to get company names based on product query.
    The number of results is set to 1 by default and can be changed by setting the 'howmany' parameter.
    """
    return StreamingResponse(
        company_name.llm_company_name(product, howmany),
        media_type = "text/event-stream"
    )
    # try:
    #     # _ = await authorize.authorize(request)

    #     res = company_name.llm_company_name(product, howmany)
    #     return res
    # except HTTPException as e:
    #     raise e 
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal Server Error") from e
