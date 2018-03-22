# -*- coding: utf-8 -*-
import json
from myknputils import *
from bs4 import BeautifulSoup
import re
import copy
from pyknp import Jumanpp

from urllib.parse import unquote

import unicodedata
import string

urlList = [
  "https://dic.pixiv.net/a/八神コウ",
  "https://dic.pixiv.net/a/涼風青葉",
  "https://dic.pixiv.net/a/滝本ひふみ",
  "https://dic.pixiv.net/a/飯島ゆん",
  "https://dic.pixiv.net/a/望月紅葉",
  "https://dic.pixiv.net/a/篠田はじめ",
  "https://dic.pixiv.net/a/遠山りん",
  "https://dic.pixiv.net/a/桜ねね",
  "https://dic.pixiv.net/a/阿波根うみこ",
  "https://dic.pixiv.net/a/鳴海ツバメ",
  "https://dic.pixiv.net/a/葉月しずく",
  "https://dic.pixiv.net/a/星川ほたる"
]


#propDictName = "propDict.dict"
#predDictName = "predDict.dict"
#urlListName = "url.list"
#DBName = "database"

propDict = None
predDict = None

class dicMaker:
    def __init__(self):
        self.DB = []

        self.genre = "NEWGAME!"

        self.uniques = []

        self.knp = my_knp_utils()

        self.jumanpp = Jumanpp()

        self.symbolReg = re.compile(r'^[!-~]+$')


    def format_text(self, text):
        text = unicodedata.normalize("NFKC", text)  # 全角記号をざっくり半角へ置換（でも不完全）

        # 記号を消し去るための魔法のテーブル作成
        table = str.maketrans("", "", string.punctuation  + "・")
        text = text.translate(table)

        return text

    def getRepName(self, tag, tags):
        f = tag.features
        if "Wikipediaエントリ" in f:
            return f["Wikipediaエントリ"]
        elif re.split('[/?+]', f["正規化代表表記"])[1] in ["もの","こと","じ","ぶつ","とき","しゃ"]:
            rpn =  re.split('[/?+]', f["正規化代表表記"])[0]
            if rpn == "物":
                rpn = "もの"
            elif rpn == "者":
                rpn = "もの"
            elif rpn == "事":
                rpn = "こと"
            return tags[tag.tag_id-1].get_surface() + rpn
        else:
            return re.split('[/?+]', f["正規化代表表記"])[0]

    def gatherUnique(self, soup):
        for _a in soup.find_all("a"):

            i = unquote(_a.get("href").split("/")[-1])
            if self.symbolReg.match(i):
                continue
            r = self.knp.get_knp_result(i)
            if "固有" in r.spec():
                self.uniques.append(i)
        print(self.uniques)

    def checkUnique(self, text):
        for u in self.uniques:
            if len(text) > 1:
                if text in u:
                    return u
        return False

    def replaceUniques(self, text):
        rText = ""
        result = self.jumanpp.analysis(text)
        for mrph in result.mrph_list():
            u = self.checkUnique(mrph.midasi)
            if u:
                rText += u
            else:
                rText += mrph.midasi
        #print (rText)
        return rText


    def processData(self, result, _topic):

        __no_k = None

        _wo_k   = None
        _ni_k   = None
        _no_k   = None
        _ga_k   = None
        _adject = None

        wo_k = None
        ni_k = None
        no_k = None
        ga_k = None
        topic = None
        adject = None



        ts = result.tag_list()
        for i in range(len(ts)):

            #print(ts[i].get_surface())

            f = ts[i].features

            # 形容詞
            if "用言" in f and "形" in f["用言"] and "ID" in f and"形" in f["ID"]:
                adject = ts[i]
            else:
                adject = None

            # ノ格
            if "係" in f and "ノ格" in f["係"]:
                if "固有" in ts[i].spec():
                    no_k = ts[i]
                else:
                    no_k = None
            else:
                no_k = None

            # 主題の有無 / ガ格
            if "解析格" in f and "ガ" in f["解析格"]:
                if "ハ" in f and "固有" in ts[i].spec():
                    topic = ts[i]
                    ga_k = None
                #elif self.checkUnique(ts[i].repname):
                #    topic = ts[i]
                #    ga_k = None
                else:
                    ga_k = ts[i]
            else:
                ga_k = None
            if "係" in f and"文末" in f["係"] or "格解析結果" in f:
                topic = None

            # ニ格
            if "二" in f:
                ni_k = ts[i]
            else:
                ni_k = None

            if "ヲ" in f:
                wo_k = ts[i]
            else:
                wo_k = None

            # 解析結果
            if _adject and "体言" in f:
                if topic:
                    self.DB.append([self.genre] + [ self.getRepName(x, ts) for x in [topic, ts[i], _adject]])
                else:
                    self.DB.append([self.genre, _topic] + [ self.getRepName(x, ts) for x in [ts[i], _adject]])

            elif __no_k:
                if _ga_k or _ni_k or _wo_k :
                    if "体言" in f:
                        self.DB.append([self.genre] + [ self.getRepName(x, ts) for x in [__no_k, _ga_k or _ni_k or _wo_k , ts[i]]])
                    elif adject:
                        self.DB.append([self.genre] + [ self.getRepName(x, ts) for x in [__no_k, _ga_k or _ni_k or _wo_k , ts[i]]])

            elif _ga_k or _ni_k or _wo_k :
                if "体言" in f:
                    if topic:
                        self.DB.append([self.genre] + [ self.getRepName(x, ts) for x in [topic, _ga_k or _ni_k or _wo_k , ts[i]]])
                    else:
                        self.DB.append([self.genre, _topic] + [ self.getRepName(x, ts) for x in [_ga_k or _ni_k or _wo_k , ts[i]]])

                elif "用言" in f and "形" in f["用言"] and ("ID" not in f or not "形" in f["ID"]):
                    if topic:
                        self.DB.append([self.genre]  +[ self.getRepName(x, ts) for x in [topic, _ga_k or _ni_k or _wo_k , ts[i]]])
                    else:
                        self.DB.append([self.genre, _topic] + [ self.getRepName(x, ts) for x in [_ga_k or _ni_k or _wo_k , ts[i]]])

            __no_k  = _no_k

            _no_k   = no_k
            _ga_k   = ga_k
            _adject = adject

    def main(self, genreName):
        #with open(propDictName) as propfd:
        #    propDict = json.load(propfd)
        #with open(predDictName) as predfd:
        #    predDict = json.load(predfd)
        #with open(urlListName) as urllfd:
        #    urlList = json.load(urllfd)
        pass

#self.genre = genreName

knp = my_knp_utils()
dm = dicMaker()

for url in urlList:
    print("=== url: " + url + " ===")

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    for htags in soup.find_all("h1"):
        htags.extract()
    for htags in soup.find_all("h2"):
        htags.extract()
    for htags in soup.find_all("h3"):
        htags.extract()
    for htags in soup.find_all("h4"):
        htags.extract()
    for htags in soup.find_all("h5"):
        htags.extract()

    for br in soup.find_all("br"):
        br.extract()

    dm.gatherUnique(soup.find(id="main"))

    #print("=== page ===")
    _strings = soup.find(id="main").get_text().split("\n")
    #print(_strings)
    strings = []
    for t in _strings:
        # 前処理
        t = t.strip()
        #t = t.replace("（","(")
        #t = t.replace("）",")")
        #t = t.replace("?", "？")
        #t = t.replace("!", "！")
        t = dm.format_text(t)
        t = t.replace("\\","")
        t = t.replace(" ","")

        if len(t.split("。")) > 2:
            for __t in t.split("。")[:-1]:
                if len(__t) < 150:
                    strings.append(dm.replaceUniques(__t))
                else:
                    ts = __t.split("、")
                    tmp = ""
                    for _t in ts:
                        tmp += _t
                        if len(tmp) > 100:
                            strings.append(dm.replaceUniques(tmp))
                            tmp = ""
                    if tmp != "":
                        strings.append(dm.replaceUniques(tmp))
        elif t == '':
            continue
        elif len(t) > 150:
            ts = t.split("、")
            tmp = ""
            for _t in ts:
                tmp += _t
                if len(tmp) > 100:
                    strings.append(dm.replaceUniques(tmp))
                    tmp = ""
            if tmp != "":
                strings.append(dm.replaceUniques(tmp))
        else:
            strings.append(dm.replaceUniques(t))

    #print(strings)
    results = knp.get_knp_results(strings)
    print("=== knp done ===",url)
    for x in results:
        dm.processData(x, url.split("/")[-1])
    print("=== analysis done ===", url)

print (dm.DB)

with open("./dic/" + dm.genre + ".dct", "w") as f:
    json.dump(dm.DB, f)
