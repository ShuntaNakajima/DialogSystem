import string
from pick_urlre import UrlName
from AccesDB import AccessToDataBase
from jwn_corpusreader import JapaneseWordNetCorpusReader
from myknputils import *
import requests, json

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
            self.jpwnc = JapaneseWordNetCorpusReader('/Users/shuntanakajima/nltk_data/corpora/wordnet','/Users/shuntanakajima/nltk_data/corpora/wordnet/wnjpn-ok.tab')
        except IOError:
            self.jpwnc = JapaneseWordNetCorpusReader('/Users/Takumi63/nltk_data/corpora/wordnet','/Users/Takumi63/nltk_data/corpora/wordnet/wnjpn-ok.tab')

        self.preprocessor = preprocessor()
        self.dialog_state = "GenreDecide"
        self.knp = my_knp_utils()

        self.url = "127.0.0.1:8080/output"

    def output(self, text, url=None):
        if url is None:
            url=self.url
        r = requests.get(url,params={"output":text})
        count = 0
        while r.status_code != 200:
            count += 1
            r = requests.get(self.url,{"output":text})
            if count > 5:
                print("通信できません")
                raise

    def start(self):
        while True:
            input_text  = self.accesDB.listen()
            output_text = self.main(input_text)
            self.output(output_text)

    def main(self, sentence):
        if self.dialog_state == "GenreDecide":
            return self.genreDeicdeDialog(sentence)

        result = self.knp.get_knp_result(self.preprocessor.incompleteSentence + sentence)

        topic = self.preprocessor.search_topic(result.tag_list())

        if topic is None:
            if self.preprocessor.GTPP[1] is None:
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
            else:
                pass
        else:
            self.preprocessor.GTPP[1] = (topic.repname.split("/")[0], "other")
            self.preprocessor.GTPP[2] = None
            self.preprocessor.GTPP[3] = None

        _property, p, g = self.preprocessor.searchProperty(result.tag_list())
        if _property is None:
            if self.preprocessor.GTPP[2] is None:
                self.preprocessor.GTPP[3] = None
        else:
            if g == "work":
                self.preprocessor.GTPP[1] = (self.preprocessor.GTPP[0], "work")
            self.preprocessor.GTPP[2] = (_property.repname.split("/")[0], "all")
            self.preprocessor.GTPP[3] = None

        predicate, p = self.preprocessor.searchPredicate(result.tag_list())
        if predicate is None:
            if _property is None and topic is None:
                pass
            else:
                self.preprocessor.GTPP[3] = None
        else:
            self.preprocessor.GTPP[3] = (predicate.repname.split("/")[0], p)

        return self.generateUtterance([topic.repname.split("/")[0] if topic else None,
                                       _property.repname.split("/")[0] if _property else None,
                                       predicate.repname.split("/")[0] if predicate else None], self.preprocessor.getInputType(result))


    def searchData(self,text):
        pass
    def generateConstraction(self, data):
        """
        発話に使用するための対比を生成する

        返値 : (A, B, C) の情報が入ったタプル
        """
        returndata = self.urlfinder.find_url(data[0])
        if data[0] and (data[1] or data[2]):
            if not data[1] and data[2]:
                results = self.accessDB.searchDB(self.GPTT[0][0],returndata,"",data[2])
                generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],result[0],bool(1))
            else:
                print((self.preprocessor.GTPP[0][0],returndata,data[1],""))
                results = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],returndata,data[1],"")
                print(results)
                maxsimirary = ''
                for result in results:
                    print(result)
                    simirary = self.jpwnc.calcSimilarity(data[2],result)
                    print(simirary)
                    if not maxsimirary:
                        maxsimirary = float(simirary[0])
                        maxsimirary_word = result
                    elif float(simirary[0]) > float(maxsimirary):
                        maxsimirary = simirary[0]
                        maxsimirary_word = result
                generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],maxsimirary_word,bool(1))
        else:
            generateddata = data + (bool(0))
    #    if data == ('青葉','髪','きれい'):
    #        generateddata = ('八神公','髪','きれい',bool(1))
    #    else:
    #        generateddata = data + (bool(0))
        print ('GeneratedConstraction!:%s,%s,%s' % (generateddata[0],generateddata[1],generateddata[2]))
        return generateddata

    def generateUtterance(self, data, inputType):
        print ("Topic", data[0], "Property", data[1], "Predicate", data[2])
        print (self.preprocessor.GTPP)
        """
        発話を生成する

        data      : (A, B, C) の情報が入ったタプル
        inputType : 入力文が 確認(100)/疑問詞質問(200)/YN質問(300)/その他(1000) ... 更新予定
        hasTopic  : Boolean, 作品内の固有表現(例:涼風青葉，など)があるかないか判定
        返値       : String
        """
        target = data[0]
        Evalu_ax = data[1]
        Evalu = data[2]
        if inputType == 1000:
            if self.preprocessor.GTPP[0] and self.preprocessor.GTPP[1] and self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3]:
                if data[0] or data[1] or data[2]:
                    contractionItem = self.generateConstraction((self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                    if contractionItem[4] == bool(1):
                        generatedString = 'あー，%sの%sが%sみたいにね' % (contractionItem[1],contractionItem[2],contractionItem[3])
                    else:
                        generatedString = 'たしかに'
                else:
                    #話題を変えましょう
                    contractionItem = self.generateConstraction((self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                    if contractionItem[4] == bool(1):
                        generatedString = 'うーん，%sの%sとか%sだけどね' % (contractionItem[1],contractionItem[2],contractionItem[3])
                    else:
                        generatedString = 'たしかに'#ここどうしよう.....
            else:
                generatedString = 'うん,'
        else:
            if inputType == 100:
                generatedString = 'あーそうだと思うよ'
                #net
            elif inputType == 200:
                generatedString = 'なんでだっけ，'
                #net
                #generateConstraction((self.preprocessor.GTPP[1],self.preprocessor.GTPP[2],self.preprocessor.GTPP[3]))
            elif inputType == 300:
                generatedString = 'うーん，どうなんだろうね...'
        return (generatedString)
