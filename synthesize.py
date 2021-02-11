import requests
import json


class KakaoSynthesize:

    def __init__(self):

        with open("AppKey", 'r') as file:
            self.appKey = json.load(file)

        self.url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
        self.headers = {
            'Content-Type': "application/xml",
            'Authorization': "KakaoAK " + self.appKey["REST_API_KEY"]
        }

    def generate(self):

        data = "<speak>테스트 중입니다</speak>"
        response = requests.post(self.url, headers=self.headers, data=data.encode("utf-8"))

        if response.status_code == 200:
            with open('media/sound/alert.mp3', 'wb') as f:
                f.write(response.content)
