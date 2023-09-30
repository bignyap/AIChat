from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from my_llm import companyname

some_file_path = "sample.mp4"
app = FastAPI()

@app.get("/")
async def title():
    return "Hello World!"


@app.get("/stream")
def stream():
    def iterfile():
        with open(some_file_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.get("/companyname")
def company_name(product: str, howmany:int = 1):
    res =  companyname.llm_company_name(product, howmany)
    return res



