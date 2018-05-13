# -*- coding: utf-8 -*-
import string
from pick_urlre import UrlName
from AccesDB import AccessToDataBase
from jwn_corpusreader import JapaneseWordNetCorpusReader
from myknputils import *
import requests, json
from numpy.random import *
from q_topic import titleName
from copy import deepcopy
from writelog import writeLog

class DialogSystem:
    """
    AのBはCという情報を対比という形で使うことで，面白い発話を作る対話システム
    """
    def __init__(self):
        #self.theme = 'NEWGAME!'
        #self.TABC = ['Topic','A','B','C']
        self.urlfinder = UrlName()
        self.accessDB = AccessToDataBase()
        try:
            self.jpwnc = JapaneseWordNetCorpusReader()
        except IOError:
            self.jpwnc = JapaneseWordNetCorpusReader('/Users/shuntanakajima/nltk_data/corpora/wordnet','/Users/shuntanakajima/nltk_data/corpora/wordnet/wnjpn-ok.tab')

        self.preprocessor = preprocessor()
        self.dialog_state = "GenreDecide"
        self.knp = my_knp_utils()

        self.url = "127.0.0.1:8080/output"

        self.genreDeicdeDialog = titleName(10)

        self.kibun = "comp" # or "symp"
        self.writelog = writeLog()


    def output(self, text, url=None):

        if self.output_type:
            print(text)
        else:
            if url is None:
                url=self.url
            print(text)
            r = requests.get(url,params={"query":text})
            count = 0
            while r.status_code != 200:
                count += 1
                r = requests.get(self.url,{"query":text})
                if count > 5:
                    # print("通信できません")
                    raise

    def start(self, debug = False,output_type = False):
        print ("======会話開始======")
        self.output_type = output_type
        while True:
            if debug:
                input_text  = input(">> ")
            else:
                input_text  = self.accessDB.listen()
            output_text = self.main(input_text)
            #--------------ログの書き出し-----------=---------
            self.writelog.writeLog('user',input_text)
            self.writelog.writeLog('system',output_text)
            #----------------------------------------------
            if debug:
                print(output_text)
            else:
                self.output(output_text)

    def main(self, sentence):
        if self.dialog_state == "GenreDecide":
            output_text, title = self.genreDeicdeDialog.getUtterance(sentence)
            if title:
                self.preprocessor.GTPP[0] = (title, None)
                self.preprocessor.setGenre(title)
                self.dialog_state = "a"
            return output_text

        result = self.knp.get_knp_result(self.preprocessor.incompleteSentence + sentence)

        ts = result.tag_list()

        #topic, topic_tag = self.preprocessor.search_topic(ts)
        if self.preprocessor.GTPP[2] is (None,None) or self.preprocessor.GTPP[2] is None:
            topic, topic_tag = self.preprocessor.search_topic_by_sentence(ts,sentence)

            if topic is None:
                if self.preprocessor.GTPP[1] is None:
                    self.preprocessor.GTPP[2] = None
                    self.preprocessor.GTPP[3] = None
                else:
                    pass
            else:
                self.preprocessor.GTPP[1] = (topic, "other")
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
                ts.remove(topic_tag)
        else:
            topic = None
            if self.preprocessor.GTPP[1] is None:
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
            else:
                pass


        _property, p, g = self.preprocessor.searchProperty(ts)
        if _property is None:
            if self.preprocessor.GTPP[2] is None:
                self.preprocessor.GTPP[3] = None
        else:
            if g == "work":
                self.preprocessor.GTPP[1] = (self.preprocessor.GTPP[0], "work")
            if self.preprocessor.GTPP[2] is None and self.preprocessor.GTPP[3] is not None:
                self.preprocessor.GTPP[2] = (_property.repname.split("/")[0], "all")
            else:
                self.preprocessor.GTPP[2] = (_property.repname.split("/")[0], "all")
                self.preprocessor.GTPP[3] = None
            ts.remove(_property)

        predicate, p = self.preprocessor.searchPredicate(ts)
        if predicate is None:
            if _property is None and topic is None:
                pass
            else:
                self.preprocessor.GTPP[3] = None
        else:
            self.preprocessor.GTPP[3] = (predicate.repname.split("/")[0], p)

        if self.preprocessor.GTPP[1] is not None and self.preprocessor.GTPP[2] is None and self.preprocessor.GTPP[3] is not None:
            result = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],"",self.preprocessor.GTPP[3][0])
            if result:
                self.preprocessor.GTPP[2] = (result[-1], "all")
                return self.generateUtterance([topic if topic else None,
                                               result[-1],
                                               predicate.repname.split("/")[0] if predicate else None], self.preprocessor.getInputType(result))


        return self.generateUtterance([topic if topic else None,
                                       _property.repname.split("/")[0] if _property else None,
                                       predicate.repname.split("/")[0] if predicate else None], self.preprocessor.getInputType(result))


    def searchData(self,text):
        pass
    def generateConstraction(self, data):
        """
        発話に使用するための対比を生成する

        返値 : (A, B, C) の情報が入ったタプル
        """
        j = self.urlfinder.find_url(data[0])

        if data[0] and (data[1] or data[2]):
            while True:
                def choose(mylist):
                    num = randint(0,len(mylist) - 1)
                    return mylist[num]
                returndata = choose(j)
                j.remove(returndata)
                if not data[1] and data[2]:
                    results = self.accessDB.searchDB(self.GTPP[0][0],returndata,"",data[2])
                    if type(results) is list:
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],result[0],bool(1))
                    elif type(results) is str:
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],result,bool(1))
                else:
                    #print((self.preprocessor.GTPP[0][0],returndata,data[1],""))

                    results = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],returndata,data[1],"")
                    print('this is testing')
                    print(results)
                    if results:
                        maxsimirary = ''
                        for result in results:
                            simirary = self.jpwnc.calcSimilarity(data[2],result)
                            print(simirary)
                            if not maxsimirary:
                                if simirary[0] != None:
                                    maxsimirary = float(simirary[0])
                                    maxsimirary_word = result
                            elif float(simirary[0]) > float(maxsimirary):
                                maxsimirary = simirary[0]
                                maxsimirary_word = result
                        print('simirary-----------')
                        print(data[2])
                        print(maxsimirary_word)
                        print(maxsimirary)
                        print('simirary-----------')
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],maxsimirary_word,bool(1))
                        break
                    else:
                        if j == []:
                            generateddata = (self.preprocessor.GTPP[0][0],) + data + (bool(0),)
                            break
        else:
            generateddata = (self.preprocessor.GTPP[0][0],) + data + (bool(0),)
    #    if data == ('青葉','髪','きれい'):
    #        generateddata = ('八神公','髪','きれい',bool(1))
    #    else:
    #        generateddata = data + (bool(0))
        print ('GeneratedConstraction!:%s,%s,%s,%s' % (generateddata[0],generateddata[1],generateddata[2],generateddata[3]))
        return generateddata

    def generateUtterance(self, data, inputType):
        print ("just before","Topic", data[0], "Property", data[1], "Predicate", data[2])
        print ("until now", self.preprocessor.GTPP)
        returnstr = []
        """
        発話を生成する

        data      : (A, B, C) の情報が入ったタプル
        inputType : 入力文が 確認(100)/疑問詞質問(200)/YN質問(300)/その他(1000) ... 更新予定
        hasTopic  : Boolean, 作品内の固有表現(例:涼風青葉，など)があるかないか判定
        返値       : String
        """

        generatedString = "うんうん!"

        def choose(mylist):
            num = randint(0,len(mylist) - 1)
            return mylist[num]
        target = data[0]
        Evalu_ax = data[1]
        Evalu = data[2]
        if inputType == 1000:
            if self.preprocessor.GTPP[0] and self.preprocessor.GTPP[1] and self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3]:
                self.kibun = "a"
                if self.kibun == "comp":
                    self.kibun = "symp"
                    contractionItem = self.generateConstraction((self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                    if contractionItem[4] == bool(1):
                        #num = randint(1,3)
                        #returnstr.append('あー，%sの%sが%sみたいにね' % (contractionItem[1],contractionItem[2],contractionItem[3]))
                        #returnstr.append('%sの%sが%sみたいなかんじ？' % (contractionItem[1],contractionItem[2],contractionItem[3]))
                        #returnstr.append('たとえば、%sの%sが、%sのようにね' % (contractionItem[1],contractionItem[2],contractionItem[3]))
                        generatedString = "確かに。でも、%sも%s%sよね" % (contractionItem[1],contractionItem[2],contractionItem[3])
                        self.kibun = "symp"
                    else:
                        generatedString = 'たしかに'
                elif self.kibun == "symp":
                    self.kibun = "a"
                    r = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0], "")
                    if r:
                        generatedString = "うんうん、%sよね" % (r[-1])

                elif data[0] or data[1] or data[2]:
                    contractionItem = self.generateConstraction((self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                    if contractionItem[4] == bool(1):
                        num = randint(1,3)
                        returnstr.append('あー，%sの%sが%sみたいにね' % (contractionItem[1],contractionItem[2],contractionItem[3]))
                        returnstr.append('%sの%sが%sみたいなかんじ？' % (contractionItem[1],contractionItem[2],contractionItem[3]))
                        returnstr.append('たとえば、%sの%sが、%sのようにね' % (contractionItem[1],contractionItem[2],contractionItem[3]))
                        generatedString = choose(returnstr)
                    else:
                        generatedString = 'たしかに'
                else:
                    #話題を変えましょう
                    contractionItem = self.generateConstraction((self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                    if contractionItem[3] == bool(1):
                        generatedString = 'うーん，%sの%sとか%sだけどね' % (contractionItem[1],contractionItem[2],contractionItem[3])
                    else:
                        returndata = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],'',self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0])
                        next_theme = ''
                        for i in returndata:
                            if self.preprocessor.GTPP[1][0] is not i:
                                next_theme = i
                        if not next_theme:
                            generatedString = 'そろそろ話題がなくなって来たなぁ'
                        else:
                            returnstr.append('%sが%sといえば%sもそうじゃなかったっけ？' % (self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0],next_theme))
                            returnstr.append('%sの%sも%sだった気がする！' % (next_theme,self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                            generatedString = choose(returnstr)
                        #ここどうしよう.....
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
            else:
                returnstr.append('うん,')
                returnstr.append('はい,')
                generatedString = choose(returnstr)
        else:
            if inputType == 100:
                if self.preprocessor.GTPP[0] and self.preprocessor.GTPP[1] and self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3]:
                    truedata = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],'')
                    print (truedata)
                    if truedata:
                        maxsimirary = ''
                        for result in truedata:
                            print (result)
                            simirary = self.jpwnc.calcSimilarity(data[2],result)
                            print('------------simi----------')
                            print(simirary)
                            print('------------simiend----------')

                            if simirary[0] == None:
                                pass
                            elif not maxsimirary:
                                maxsimirary = float(simirary[0])
                                maxsimirary_word = result
                            elif float(simirary[0]) > float(maxsimirary):
                                maxsimirary = simirary[0]
                                maxsimirary_word = result
                        print(maxsimirary)
                        if maxsimirary > 0.06:
                            if maxsimirary == 1:
                                returnstr.append('そうだとおもうよ')
                                returnstr.append('あーそうだね')
                                generatedString = choose(returnstr)
                            else:
                                returnstr.append('え？%sじゃなっかったっけ' % maxsimirary_word)
                                returnstr.append('%sじゃなくて%sじゃなっかったっけ' % (self.preprocessor.GTPP[3][0],maxsimirary_word))
                                generatedString = choose(returnstr)
                        else:
                            generatedString = 'んーどうだっけ、忘れちゃった'
                    else:
                        generatedString = 'んーどうだっけ、忘れちゃった'
                #net
            elif inputType == 200:
                total_object = 0
                for dt in data:
                    if dt:
                        total_object = total_object + 1
                if data[0] and data[1] and data[2]:
                    generatedString = 'うーん、わからない，'
                else:
                    if data[0] and self.preprocessor.GTPP[2][0] and self.preprocessor.GTPP[3][0]:
                        generatedString = 'ごめん、わからない、'
                    elif not data[0] and self.preprocessor.GTPP[1][0] is None:
                        generatedString = 'だれの？'
                    elif not data[0]:
                        if self.preprocessor.GTPP[2][0] and self.preprocessor.GTPP[3][0]:
                            generatedString = 'あー，たしかに%sだよね、なんでだろう' % self.preprocessor.GTPP[3][0]
                        elif data[1]:
                            dbdata = self.accessDB.searchDB(self,self.preprocessor.GTPP[1][0],data[1],data[2],"")
                            generatedString = '%sだからじゃない？' % dbdata[0]
                    else:
                        generatedString = 'わからない'

                #なんで涼風青葉の髪は長く鳴った
                #net
                #generateConstraction((self.preprocessor.GTPP[1],self.preprocessor.GTPP[2],self.preprocessor.GTPP[3]))
            elif inputType == 300:
                returnstr.append('うーん，どうなんだろうね')
                returnstr.append('なんでだろう、知らない')
                generatedString = choose(returnstr)
        return (generatedString)
