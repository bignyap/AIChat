from fastapi import FastAPI, UploadFile
from CompanyName import CompanyName
from Summarizer import Summarizer

app = FastAPI()

@app.get("/getCompanyName")
def company_name(product: str, howmany:int = 1):
    return CompanyName.llm_company_name(product, howmany)


@app.post("/summarize")
async def llm_summarize(file: UploadFile):
    filepath = await Summarizer.PDFReader(file)
    res =  Summarizer.PDFSummarizer(filepath)
    return res
    



