import os

import hashlib
from urllib.parse import urlencode

import upbit
import time
import requests
import json

serverURL = "https://api.upbit.com"

account = upbit.Upbit(serverURL)
print(json.dumps(account.getAccount(), indent=4))
print(account.getAssetsList())

print(account.getTicker("KRW-BTC"))



while(True):
    time.sleep(0.2)
    # print(account.getTradePrice("KRW-BTC"))
    # print(account.analyzeMinuteCandle("KRW-BTC", 1, 3))
    print(account.getAssetValuation("KRW-BTC"))

# url = "https://api.upbit.com/v1/candles/minutes/1"
#
# querystring = {"market":"KRW-BTC","count":"30"}
#
# response = requests.request("GET", url, params=querystring)
#
# jsonObject = response.json()
#
# print(json.dumps(jsonObject, indent=4))
#
#
#
