#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import types

from AccesDB import AccessToDataBase

ADB = AccessToDataBase()

url2 = "http://192.168.11.14:8080"

KEY = '55702e566f352f5744767a71644d32796f544a58506866716b776d7569726e33544b7538427652414a7943'

#エンドポイントの設定
endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
url = endpoint.replace('REGISTER_KEY', KEY)

#1回目の会話の入力
#utt_content = ADB.listen()
utt_content = input()

payload = {'utt' : utt_content, 'context': ''}
headers = {'Content-type': 'application/json'}

#送信
r = requests.post(url, data=json.dumps(payload), headers=headers)
data = r.json()

#jsonの解析
response = data['utt']
context = data['context']

#output
print(response)
count = 0

print(response)

#2回目以降の会話(Ctrl+Cで終了)
while True:
    #utt_content = ADB.listen()
    utt_content = input()

    payload['utt'] = utt_content
    payload['context'] = data['context']

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()

    response = data['utt']
    context = data['context']
    print(response)
    #output

    count = 0

    print(response)
