import jwt, uuid, json, requests, math


class Upbit:

    def __init__(self, serverURL):

        self.serverURL = serverURL # 서버 URL을 지정합니다
        self.headers = {}

        with open("Accesskey", 'r') as jsonFile:
            self.accessKey = json.load(jsonFile) # 외부파일에서 accessKey를 불러옵니다

    def setNonce(self):
        """
        nonce 필드의 값으로 무작위 UUID 문자열을 이용합니다.
        nonce는 단 한 번만 사용되므로 조회 시마다 새로운 nonce를 생성하여 인증된 header를 만듭니다
        :return: NULL
        """
        payload = {
            'access_key': self.accessKey["access_key"],
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, self.accessKey["secret_key"])
        authorize_token = 'Bearer {}'.format(jwt_token)
        self.headers = {"Authorization": authorize_token}

    def getAccount(self):
        self.setNonce()
        response = requests.get(self.serverURL + "/v1/accounts", headers=self.headers)
        return response.json()

    def getAssetsList(self):
        """
        현재 보유하고 있는 자산을 조회합니다.
        :return: 보유자산을 리스트로 반환합니다.
        """
        self.setNonce()
        response = requests.get(self.serverURL + "/v1/accounts", headers=self.headers)
        list = []

        for data in response.json():
            list.append(data["currency"])

        return list

    def getTicker(self, markets):
        params = {"markets": markets}
        response = requests.request("GET", self.serverURL + "/v1/ticker", params=params)
        return response.json()

    def getTradeInfo(self, markets):
        params = {"markets": markets}
        response = requests.request("GET", self.serverURL + "/v1/ticker", params=params)
        jsonObject = response.json()
        return {"tradePrice": jsonObject[0]["trade_price"],"change": jsonObject[0]["change"], "changeRate":jsonObject[0]["signed_change_rate"]}

    def getTradePrice(self, markets):
        params = {"markets": markets}
        response = requests.request("GET", self.serverURL + "/v1/ticker", params=params)
        jsonObject = response.json()
        return jsonObject[0]["trade_price"]

    def getMinuteCandle(self, market, minute, count, to=""):
        params = {"market": market, "count": str(count), "to": str(to)}
        response = requests.request("GET", self.serverURL + "/v1/candles/minutes/" + str(minute), params=params)
        return response.json()

    def analyzeMinuteCandle(self, market, minute, count):
        """
        변화율 및 변화 기준은 전 분봉의 종가 기준
        :param market:
        :param minute:
        :param count:
        :return: ["변화", 백분율 변화율, 변화율]
        """
        count = count + 1
        minuteList = []
        tempList = []
        params = {"market": market, "count": str(count)}
        response = requests.request("GET", self.serverURL + "/v1/candles/minutes/" + str(minute), params=params)
        minuteCandle = response.json()

        for i in range(len(response.json())-1, 0, -1):

            if minuteCandle[i]["trade_price"] > minuteCandle[i-1]["trade_price"]:
                tempList.append("FALL")
            elif minuteCandle[i]["trade_price"] < minuteCandle[i-1]["trade_price"]:
                tempList.append("RISE")
            else:
                tempList.append("EVEN")

            ratio = (minuteCandle[i - 1]["trade_price"] - minuteCandle[i]["trade_price"]) / minuteCandle[i-1]["trade_price"]
            tempList.append(round(ratio*100, 2))
            tempList.append(ratio)


            minuteList.append(tempList)
            tempList = []

        return minuteList

    def getAssetValuation(self, market):
        """

        :param market: 줄표로 구분되는 마켓 코드
        :return: [총매수, 총평가, 수익률, 평가손익]
        """
        self.setNonce()
        response = requests.get(self.serverURL + "/v1/accounts", headers=self.headers)
        list = []


        for data in response.json():

            if data["currency"] == market.split("-")[1]:
                assetPosition = data["avg_buy_price"]
                presentPrice = self.getTradePrice(market)
                difference = (presentPrice-float(assetPosition))
                valuation = float(presentPrice-float(assetPosition)) * float(data["balance"])

                list.append(math.ceil(float(data["avg_buy_price"]) * float(data["balance"])))
                list.append(math.floor(presentPrice * float(data["balance"])))
                list.append(round(difference / float(assetPosition)*100, 2))
                list.append(math.floor(valuation))

                return list

            return None

    def getRSI(self, length=14, count=200):
        preMinuteData = self.getMinuteCandle("KRW-BTC", 1, count)

        dataList = []
        rsiList = []

        for i in range(length-1):
            rsiList.append(None)

        riseList = [0, ]
        fallList = [0, ]

        for i in range(len(preMinuteData)):
            dataList.append({"time" : preMinuteData[len(preMinuteData) - 1 - i]['candle_date_time_kst'].replace("T", " "),
                             "tradePrice" : preMinuteData[len(preMinuteData) - 1 - i]['trade_price']})

            if 0 <= i <= length-1:
                dataList[i]['difference'] = dataList[i]['tradePrice'] - dataList[i-1]['tradePrice']

                if i < length-1 :

                    if dataList[i]['difference'] > 0:
                        riseList.append(abs(dataList[i]['difference']))
                        fallList.append(0)
                    else:
                        fallList.append(abs(dataList[i]['difference']))
                        riseList.append(0)

                if i == length - 1:

                    dataList[i]['AU'] = sum(riseList)
                    dataList[i]['AD'] = sum(fallList)
                    dataList[i]['rsi'] = (100 * dataList[i]['AU'] / (dataList[i]['AU'] + dataList[i]['AD']))

                elif i == 0:
                    dataList[i]['difference'] = 0

            elif i >= length:

                dataList[i]['difference'] = dataList[i]['tradePrice'] - dataList[i - 1]['tradePrice']

                if dataList[i]['difference'] > 0:

                    dataList[i]['AU'] = (dataList[i-1]['AU'] * (length - 1) + abs(dataList[i]['difference'])) / length
                    dataList[i]['AD'] = ((dataList[i-1]['AD'] * (length - 1)) / length)

                else:

                    dataList[i]['AU'] = ((dataList[i-1]['AU'] * (length - 1)) / length)
                    dataList[i]['AD'] = (dataList[i-1]['AD'] * (length - 1) + abs(dataList[i]['difference'])) / length

                dataList[i]['rsi'] = (100*dataList[i]['AU']/(dataList[i]['AU']+dataList[i]['AD']))



        #
        # for i in range(len(dataList)):
        #     print(i, end = "")
        #     print(dataList[i])

        import sys
        print(sys.getsizeof(dataList))
        return dataList[len(dataList)-1]['rsi']





