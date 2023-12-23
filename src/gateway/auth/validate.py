''' Validate access token  for each request through the gateway ''' 

import os
import requests


AUTH_SVC_ADDRESS = os.environ.get('AUTH_SVC_ADDRESS')
TIMEOUT_LIMIT = int(os.environ.get('TIMEOUT_LIMIT'))

def token(request):
    ''' get token from the request and validate'''
    
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    access_token = request.headers["Authorization"]

    if not access_token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://{AUTH_SVC_ADDRESS}/validate",
        headers={"Authorization": access_token},
        timeout = TIMEOUT_LIMIT
    )

    if response.status_code == 200:
        return response.text, None
        
    return None, (response.text, response.status_code)