#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import types
from writelog import writeLog
from AccesDB import AccessToDataBase

ADB = AccessToDataBase()

url2 = "http://192.168.11.14:8080"

KEY = '55702e566f352f5744767a71644d32796f544a58506866716b776d7569726e33544b7538427652414a7943'

#エンドポイントの設定
endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
url = endpoint.replace('REGISTER_KEY', KEY)

utt_content = ''
payload = {'utt' : utt_content, 'context': ''}
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
data = r.json()
writelog = writeLog('docomo')
while True:
    utt_content = ADB.listen()
    #utt_content = input()

    payload['utt'] = utt_content
    #payload['context'] = data['context']

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()

    response = data['utt']
    context = data['context']
    #output

    count = 0
    #--------------ログの書き出し-----------=---------
    writelog.writeLog('user',utt_content)
    writelog.writeLog('system',response)
    #----------------------------------------------
    requests.get(url2,params={"query":response})
    print(response)
