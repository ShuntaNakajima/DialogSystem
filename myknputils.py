# -*- coding: utf-8 -*-
import json, re, requests
from knp_utils import knp_job,models, KnpSubProcess
from pyknp import KNP
from bs4 import BeautifulSoup
from AccesDB import AccessToDataBase

class my_knp_utils:
    def __init__(self):
        self.knp = KNP()
        #self.IDsetter = counter()
        self.__counter__ = 0

    def counter(self):
        self.__counter__ += 1
        return self.__counter__



    # about input
    def get_knp_result(self, sentence, id = 0):
        # print('before: ' + sentence)
        sentence = sentence.replace(' ', '')
        sentence = sentence.replace('   ', '')
        sentence = sentence.replace(' ', '')
        # print('after: ' + sentence)
        g = input_str=knp_job.main([{"text-id":self.counter(), "text":sentence}], juman_command="jumanpp", knp_options="-tab -anaphora").seq_document_obj[0].parsed_result
        #print('after2: ' + g)
        r = self.knp.result(g)
        for t in r.tag_list():
            pass
            #print(t.repname)
        return r

    def get_knp_results(self, sentences, id = 0):
        return [self.knp.result(input_str=x.parsed_result) for x in knp_job.main([{"text-id":self.counter(), "text":x} for x in sentences], juman_command="jumanpp", knp_options="-tab -anaphora").seq_document_obj]

    def get_nodes_from_terminal(self, knp_tag):
        tags = []
        for t in knp_tag.children:
            tags += self.get_nodes_from_terminal(t)
        return tags + [knp_tag]

    def get_kframe(self, tag, kFrameName):
        """
        引数:
          "ガ","デ" .... "時間", "外の関係", "修飾", "トスル", "二ツク", .....
          述語の品詞によって異なる？ 単語によっても異なるかも
        返値: (単語, tag-id)
          述語でない場合                        : None
          指定した格フレームは取り得ない場合      : ''
          指定した格フレームは取っていなかった場合 : '-'
          指定した各フレームを持つ場合            : 'word'
        """
        if "格解析結果" not in tag.features:
            return (None, None)
        r = re.search("%s/[^/]+/([^/]+)/([^/]+)/[^/]+/[^/]+;" % kFrameName, tag.features["格解析結果"])
        if r is None:
            return ("", None)
        else:
            return (r.group(1), None if r.group(2) == "-" else int(r.group(2)))

    def get_modify_type(self, tag):
        """
        返値:
          文節内 / ノ格 / 〇〇格 / (副詞とかもあるかも)
        """
        if "係" in tag.features:
            return tag.features["係"]
        else:
            return None


class preprocessor:

    def __init__(self):
        self.knp = KNP()
        self.util = my_knp_utils()
        self.db = AccessToDataBase()
        self.uniques = ["八神コウ"]
        self.topicDict = {}
        self.incompleteSentence =""

        self.GTPP = [None]*4

        # 属性データベース
        self.propertyDicts = {
            "work"  : {},
            "other" : {"髪": "all","目":"all","仕事":"all"}
        }
        """
        {
          "work": {B: 種類, ....},
          Aの種類 : {B: 種類, ....},
          ...
        }
        今は other だけ
        """


        # 述語データベース
        self.predicateDict = {
            "短い": "all",
            "長い": "all",
            "黄色": "all",
            "青色": "all",
            "黄": "all",
            "青": "all",
            "頑張っている":"all"
        }
        """
        {
          ”C”: 種類,
          ...
        }
        今は all だけ
        """

        # webページキャッシュ
        self.cashe = {}

    def checkUnique(self, text):
        for u in self.uniques:
            if len(text) > 1:
                if text in u:
                    return u
        return False


    def setGenre(self, genre):
        result = self.db.getData(genre)
        # print(result.val().items())
        for topic, pp in result.val().items():
            self.uniques.append(topic)
            for k, v in pp.items():
                if type(k) is list:
                    for i in k:
                        self.propertyDicts["other"][i] = "all"
                else:
                    self.propertyDicts["other"][k] = "all"
                    
                if type(v) is list:
                    for i in v:
                        self.predicateDict[i] = "all"
                else:
                    self.predicateDict[v] = "all"
        del self.propertyDicts["other"]["青葉"]
        del self.predicateDict["キャラ"]
        print(self.propertyDicts, self.predicateDict)

    # about result
    def search_topic_candidate(self, tagList):
        cand_list = []

        '''
        # ガ格, ガ格を修飾する名詞全てを候補
        for t in tagList[::-1]:
            kframe, index = self.util.get_kframe(t, "ガ")
            if kframe is None:
                continue
            elif index is None:
                continue
            else:
                cand_list += [t]
                for t in self.util.get_nodes_from_terminal(tagList[index])[:-1]:
                    mType = self.util.get_modify_type(t)
                    if mType == "ノ格":
                        # 固有名詞があれば検索の優先度をあげる
                        if "固有" in  t.spec():
                            cand_list =  [t] + cand_list
                        else:
                            cand_list += [t]
                    elif mType == "文節内":
                        pass
                    else:
                        return cand_list
                return cand_list

        for t in tagList:
            if "固有" in  t.spec():
                return [t]

        return []

        '''

        rList = []

        for t in tagList:
            text = t.repname.split("/")[0]
            for u in self.uniques:
                if len(text) > 1:
                    if text in u:
                        rList.append((t, u))
                        continue
            """
            if "固有" in t.spec():
                rList.append((t, t.repname.split("/")[0]))
            """
        return rList
    
    def search_topic(self, tagList):
        lst = self.search_topic_candidate(tagList)
        # print("candidate", lst)
        for word in lst:
            if self.isTopic(word[1]):
                return (word[1], word[0])
        return (None, None)

    def isTopic(self, word):
        if self.GTPP[1] is not None:
            if word in self.propertyDicts[self.GTPP[1][1]]:
                return False
        else:
            for dicts in self.propertyDicts:
                if word in dicts:
                    return False

        if word in self.predicateDict:
            return False

        return True

        
        
    def isTopicWithTag(self, tag):
        # dict check
        if self.GTPP[1] is not None:
            if tag.repname.split("/")[0] in self.propertyDicts[self.GTPP[1][1]]:
                return False
        else:
            for dicts in self.propertyDicts:
                if tag.repname.split("/")[0] in dicts:
                    return False

        if tag.repname.split("/")[0] in self.predicateDict:
            return False


        # use genre_page / pixiv only?
        for page in self.genrePages:
            soup = BeautifulSoup(page, 'lxml')
            aTags = soup.find_all("a", text=re.compile(tag.repname.split("/")[0]))
            for _a in aTags:
                # pixiv only
                r = None
                if _a.get("href") in self.cashe:
                    r = self.cashe[_a.get("href")]
                else:
                    _r = requests.get(_a.get("href"))
                    if _r.status_code == 200:
                        r = _r.text
                        self.cashe[_a.get("href")] = r
                    else:
                        continue
                soup = BeautifulSoup(r, 'lxml')
                cl = soup.find(id="breadcrumbs").find_all("a")
                for c in cl[::-1]:
                    if self.GTPP[0][0] in c.text:
                        return True
                    else:
                        pass

        # search page
        r = None
        url = "https://dic.pixiv.net/a/" + tag.repname.split("/")[0]
        # print("url", url)
        if url in self.cashe:
            r = self.cashe[url]
        else:
            _r = requests.get(url)
            #print("respond", _r.status_code, _r.text)
            if _r.status_code == 200:
                r = _r.text
                self.cashe[url] = r
            else:
                return False
        soup = BeautifulSoup(r, 'lxml')
        cl = soup.find(id="breadcrumbs").find_all("a")
        for c in cl[::-1]:
            if self.GTPP[0][0] in c.text:
                return True
        return False

    def searchProperty(self, tagList):
        for tag in tagList:
            p, g = self.isProperty(tag)
            if p:
                return (tag, p, g)
        return (None, None, None)

    def isProperty(self, tag):
        if self.GTPP[1] is not None:
            if tag.repname.split("/")[0] in self.propertyDicts[self.GTPP[1][1]]:
                return (self.propertyDicts[self.GTPP[1][1]][tag.repname.split("/")[0]], self.GTPP[1][1])
        else:
            if tag.repname.split("/")[0] in self.propertyDicts["work"]:
                return (self.propertyDicts["work"][tag.repname.split("/")[0]], "work")
        return (False, None)



    def searchPredicate(self, tagList):
        for tag in tagList:
            p = self.isPredicate(tag)
            if p:
                return (tag, p)
        return (None, None)

    def isPredicate(self, tag):
        if tag.repname.split("/")[0] in self.predicateDict:
            if self.GTPP[2] is None:
                return self.predicateDict[tag.repname.split("/")[0]]
            elif self.GTPP[2][1] == self.predicateDict[tag.repname.split("/")[0]]:
                return self.predicateDict[tag.repname.split("/")[0]]
        return False

    

    def getInputType(self, result):
        return 1000
        text = result
        for pt in ["よね", "でしょ", "もんね", "かね", "かな", "じゃない"]:
            if pt in text:
                return 100
        string = ""
        for tag in result.tag_list():
            string += tag.get_surface()
        for pt in ["なに","なぜ","どれ" "どこ", "なんで", "どうして","だれ","誰","何の","なんの"]:
            if pt in string:
                return 200
        for pt in ["なの","ですか"]:
            if pt in text:
                return 300
        return 1000
