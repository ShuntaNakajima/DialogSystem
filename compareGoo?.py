#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import json
import requests
from io import StringIO
import re
import time

from AccesDB import AccessToDataBase

ADB = AccessToDataBase()

url2 = "http://192.168.11.14:8080"

config = {
  "apiKey": "AIzaSyDqmJ2l6ojiTpJo5NQr0z7Lsmy2x5ONX4A",
  "authDomain": "cozmo-f3c99.firebaseapp.com",
  "databaseURL": "https://cozmo-f3c99.firebaseio.com",
  "storageBucket": ""
}


#1回目の会話の入力
#utt_content = ADB.listen()
#utt_content = input()
while True:
    utt_content = ADB.listen()
    print('User>> ' + utt_content)
    botparams = {
    "appkey": "326f020d66b10898722469403a9f8c36",
    "text": utt_content,
    }
    botp = urllib.parse.urlencode(botparams)
    boturl = "https://www.cotogoto.ai/webapi/noby.json?" + botp
    with urllib.request.urlopen(boturl) as res:
        html = res.read().decode("utf-8")
        global data
        data = json.loads(html)
    print(data["text"])
    r = requests.get(url2,params={"output":data["text"]})
    count = 0
    while r.status_code != 200:
        count += 1
        r = requests.get(url2,{"output":data["text"]})
        if count > 5:
            print("通信できません")
            raise
