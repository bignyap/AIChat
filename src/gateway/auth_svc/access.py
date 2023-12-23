''' Login for gateway '''

import os
import requests


AUTH_SVC_ADDRESS = os.environ.get('AUTH_SVC_ADDRESS')
TIMEOUT_LIMIT = int(os.environ.get('TIMEOUT_LIMIT'))


def login(request):
    ''' Login for gateway requests '''

    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    beaer_auth = (auth.username, auth.password)

    response = requests.post(
        f"http://{AUTH_SVC_ADDRESS}/login", 
        auth = beaer_auth,
        timeout = TIMEOUT_LIMIT
    )

    if response.status_code == 200:
        return response.text, None

    return None, (response.text, response.status_code)