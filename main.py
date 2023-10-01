from fastapi import FastAPI, UploadFile
from CompanyName import company_name
from PDFSummarizer import pdf_summarizer

app = FastAPI()

@app.get("/getCompanyName")
def llm_name(product: str, howmany:int = 1) -> str:
    """
    This is a docstring for llm_name.

    Args:
        product (str): string

    Returns:
        str: Path to the audio file
    """
    return company_name.llm_company_name(product, howmany)


@app.post("/summarize")
async def llm_summarize(file: UploadFile) -> str:
    """
    This is a docstring for llm_summarize.

    Args:
        file (UploadFile): UplaodFile

    Returns:
        str: Path to the audio file
    """
    filepath = await pdf_summarizer.PDFReader(file)
    res =  pdf_summarizer.PDFSummarizer(filepath)
    return res
    



