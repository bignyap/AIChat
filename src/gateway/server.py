''' Gatway doc string'''

from fastapi import FastAPI, Request, UploadFile

from auth_svc import access
from company_name import company_name
from pdf_summarizer import pdf_summarizer

app = FastAPI()

@app.post("/login")
async def login(
    request: Request
):
    ''' doc string '''

    token, err = access.login(request)

    if not err:
        return token
    
    return err


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
    filepath = await pdf_summarizer.pdf_reader(file)
    res =  pdf_summarizer.pdf_summarizer(filepath)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)