import upbit
import time
import json
# 
serverURL = "https://api.upbit.com"

account = upbit.Upbit(serverURL)
# print(json.dumps(account.getAccount(), indent=4))
# print(account.getAssetsList())
# 
# print(account.getTicker("KRW-BTC"))
# 
# 
#


# account.test()



while(True):
    print(round(account.getRSI(),2))
    time.sleep(0.1)


    # account.test()
    # print(account.analyzeMinuteCandle("KRW-BTC", 1, 3))
    # print(account.getAssetValuation("KRW-BTC"))



import synthesize

import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
label = QLabel("Hello")
label.show()

alert = synthesize.KakaoSynthesize()
alert.generate()


app.exec_()