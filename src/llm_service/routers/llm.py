''' llm endpoints '''

from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import StreamingResponse

# from i_authorize import authorize
from company_name.company_name import llm_company_name
from pdf_summarizer.pdf_summarizer import pdf_summarizer, pdf_reader
from audio_to_text.audio_to_text import audio_to_text

from .limiter import limiter


router = APIRouter(
    prefix="/llm",
)


@router.post("/summarize")
@limiter.limit("1/second")
async def llm_summarize(
    request: Request, 
    file: UploadFile
) -> str:
    """
    Endpoint to summarize a PDF file.
    
    """
    filepath = pdf_reader(file)
    res = pdf_summarizer(filepath)

    return res


@router.post("/getCompanyName")
@limiter.limit("1/second")
async def company_name_stream(
    request: Request, 
    product: str, howmany:int = 1
) -> str:
    """
    Endpoint to get company names based on product query.
    The number of results is set to 1 by default and can be changed by setting the 'howmany' parameter.
    """
    return StreamingResponse(
        llm_company_name(product, howmany),
        media_type = "text/event-stream"
    )


@router.post("/audioToText")
@limiter.limit("1/second")
async def llm_audio_to_text(
    request: Request, 
    file: UploadFile
) -> str:
    """
    Endpoint to convert speech text.
    
    """
    filepath = pdf_reader(file)
    res = audio_to_text(filepath)

    return res