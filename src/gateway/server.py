''' Gatway doc string'''

import json

from fastapi import FastAPI, Request

from auth import validate
from auth_svc import access
from company_name import company_name

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


@app.post("/nameCompanies")
async def name_companies(
    request: Request
):
    ''' company name endpoint '''

    validation, err = validate.token(request)

    if err:
        return err

    validation = json.loads(validation)

    return validation


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)