import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests

access_key = "4FqHZKOjjPqDBhjxD56E8FYnvT5Ikg8XgUtlhWsy"
secret_key = "XbdgoRmO7ddwMTEfYsRJty8wKh62XxEclZaCShRx"
server_url = "https://api.upbit.com"

# payload = {
#     'access_key': access_key,
#     'nonce': str(uuid.uuid4()),
# }
#
# jwt_token = jwt.encode(payload, secret_key)
# authorize_token = 'Bearer {}'.format(jwt_token)
# headers = {"Authorization": authorize_token}
#
# res = requests.get(server_url + "/v1/accounts", headers=headers)
#
# print(res.json())

url = "https://api.upbit.com/v1/ticker"
params = {"markets" : "KRW-BTC"}

response = requests.request("GET", url, params=params)

print(response.status_code)
print(response.text)