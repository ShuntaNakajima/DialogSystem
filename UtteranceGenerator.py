# -*- coding: utf-8 -*-
import string
from pick_urlre import UrlName
from AccesDB import AccessToDataBase
from jwn_corpusreader import JapaneseWordNetCorpusReader
from myknputils import *
import requests, json
from random import *
from q_topic import titleName
from copy import deepcopy
from writelog import writeLog

def choose(mylist):
    if len(mylist) == 0:
        return None
    num = randint(0,len(mylist) - 1)
    return mylist[num]
    


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

        self.genreDeicdeDialog = titleName(100)

        self.rFlg = True
        self.comp = False
        self.mCounter = 0

        
        self.writelog = writeLog()

        self.debug = False


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
        self.debug = debug
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

        ##### Genreを決める会話 #####
        if self.dialog_state == "GenreDecide":
            output_text, title = self.genreDeicdeDialog.getUtterance(sentence)
            if title:
                self.preprocessor.GTPP[0] = (title, None)
                self.preprocessor.setGenre(title)
                self.dialog_state = "a"
            return output_text



        
        ##### 提案手法を用いる場合 #####

        # START DEBUG
        if self.debug:
            print("\n=====現在までに得た会話情報=====\n",
                  self.preprocessor.GTPP[0],
                  self.preprocessor.GTPP[1],
                  self.preprocessor.GTPP[2],
                  self.preprocessor.GTPP[3])
        # END DEBUG

        
        ############################
        ####### 入力文の前処理 #######
        ############################
        
        # 形態素解析を実行
        result = self.knp.get_knp_result(self.preprocessor.incompleteSentence + sentence)
        # 形態素解析の結果を取得
        ts = result.tag_list()

        input_type = self.preprocessor.getInputType(result)

        # START DEBUG
        if self.debug:
            print("\n=====入力の種類=====\n",
                  input_type)
        # END DEBUG
        

        ############################
        ### 直前の会話から情報を得る ###
        ############################
        
        # 属性がまだ埋まっていない場合
        if self.preprocessor.GTPP[2] is (None,None) or self.preprocessor.GTPP[2] is None:
            # topicに相当するものを取得
            topic, topic_tag = self.preprocessor.search_topic_by_sentence(ts,sentence)
            # topicが取得できなかった場合
            if topic is None:
                # まだtopicが埋まっていない場合
                if self.preprocessor.GTPP[1] is None:
                    # topic以下を空にする
                    self.preprocessor.GTPP[2] = None
                    self.preprocessor.GTPP[3] = None
                # すでにtopicが埋まっている場合
                else:
                    # 現状維持
                    pass
            # topicが取得できた場合
            else:
                # topicを埋めて，それまでの情報は破棄
                self.preprocessor.GTPP[1] = (topic, "other")
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
                # predicateで多重で判定しないようにtopicを削除
                ts.remove(topic_tag)
                
        # 属性に当たるものが埋まっている場合
        else:
            # topicが無しにする
            topic = None
            # まだtopicが埋まっていない場合
            if self.preprocessor.GTPP[1] is None:
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
            # すでにtopicが埋まっている場合
            else:
                # 現状維持
                pass

        # propertyに相当するものを取得
        _property, p, g = self.preprocessor.searchProperty(ts)
        # propertyに相当するものを取得できなかった場合
        if _property is None:
            # まだpropertyが埋まっていない場合
            if self.preprocessor.GTPP[2] is None:
                # predicateも破棄
                self.preprocessor.GTPP[3] = None
        # propertyに相当するものを取得できた場合
        else:
            # ほんとは情報の種類によって分岐していたけど，今回はallしか使わないので実質無し
            if g == "work":
                self.preprocessor.GTPP[1] = (self.preprocessor.GTPP[0], "work")
            # キャラクタに関してのpropertyの場合
            else:
                # propertyを更新して，predicateを削除
                self.preprocessor.GTPP[2] = (_property.repname.split("/")[0], "all")
                self.preprocessor.GTPP[3] = None
            # prediacteで多重判定しないように削除
            ts.remove(_property)

        # predicateに相当するものを取得
        predicate, p = self.preprocessor.searchPredicate(ts)
        # predicateに相当するものを取得できた場合
        if predicate is not None:
            # predicateを追加
            self.preprocessor.GTPP[3] = (predicate.repname.split("/")[0], p)

        # START DEBUG
        if self.debug:
            print("\n=====直前の会話から得た情報======\n",
                  topic,
                  _property and _property.repname.split("/")[0],
                  predicate and predicate.repname.split("/")[0])
        # END DEBUG
        

        ########################
        ### propertyの補完する ###
        ########################

        result = None
        if self.preprocessor.GTPP[1] is not None and self.preprocessor.GTPP[2] is None and self.preprocessor.GTPP[3] is not None:
            result = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],"",self.preprocessor.GTPP[3][0])

            # START DEBUG
            if self.debug:
                print("\n=====補完して得た情報=====\n",
                      None,
                      result and result[-1],
                      None)
            # END DEBUG
            
            if result:
                self.preprocessor.GTPP[2] = (result[-1], "all")

            
        # START DEBUG
        if self.debug:
            print("\n=====確定した会話情報=====\n",
                  self.preprocessor.GTPP[1],
                  self.preprocessor.GTPP[2],
                  self.preprocessor.GTPP[3])
            print("\n=====出力=====\n")
        # END DEBUG        

        __prop =  _property.repname.split("/")[0] if _property else None
        return self.generateUtterance([topic,
                                       result[-1] if result else __prop,
                                       predicate.repname.split("/")[0] if predicate else None], input_type)


    def searchData(self,text):
        pass

    def generateSympathicWord(self, key):
        
        result = None
        if key == 1:
            result = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],"",self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0])
        elif key == 2:
            result = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],"",self.preprocessor.GTPP[3][0])
        elif key == 3:
            result = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],"")
        
        if type(result) is str:
            if result == self.preprocessor.GTPP[key][0]:
                return None
            else:
                simirary = self.jpwnc.calcSimilarity(self.preprocessor.GTPP[key][0],result)
                if simirary[0] is None:
                    return (result, 0)
                else:
                    return (result, 1)
                
        elif type(result) is list:
            if self.preprocessor.GTPP[key][0] in result:
                result.remove(self.preprocessor.GTPP[key][0])
            w = ""
            maxsimirary_word = ''
            for w in result:
                if w is None:
                    continue
                simirary = self.jpwnc.calcSimilarity(self.preprocessor.GTPP[key][0],w)
                if len(maxsimirary_word) == 0:
                    if simirary[0] != None:
                        maxsimirary = float(simirary[0])
                        maxsimirary_word = w
                elif simirary[0] and float(simirary[0]) > float(maxsimirary):
                    maxsimirary = simirary[0]
                    maxsimirary_word = w
            if maxsimirary_word != "":
                return (maxsimirary_word, 1)
            elif w != "":
                return (w, 0)
            else:
                return None

        
    def generateConstraction(self, data):
        """
        発話に使用するための対比を生成する

        返値 : (A, B, C) の情報が入ったタプル
        """
        
        # 比較対象となるキャラ名を取得
        j = self.urlfinder.find_url(data[0])
        generateddata = (None, None, None, None, bool(0))

        # 会話データが全部埋まっているか？
        if data[0] and (data[1] or data[2]):
            while True:
                # 比較するものを選択
                returndata = choose(j)
                if returndata is None:
                    break
                # 選択したものは除去
                j.remove(returndata)

                # propertyが足りない場合
                if not data[1] and data[2]:
                    # propertyに当たるものを検索
                    results = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],returndata,"",data[2])
                    # 検索結果が複数の場合
                    if type(results) is list:
                        # 一つ選んで比較情報にする (A',B',C)
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,choose(result),data[2],bool(1))
                    # 検索結果が一つの場合
                    elif type(results) is str:
                        # 結果を元に比較情報にする (A',B',C)
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,result,data[2],bool(1))
                # predictが足りない場合 or 全部ある場合
                else:
                    # predict候補を検索
                    results = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],returndata,data[1],"")
                    if type(results) is list and len(results) != 0:
                        maxsimirary_word = ''

                        for result in results:
                            print(result)
                            simirary = self.jpwnc.calcSimilarity(data[2],result)
                            #print(simirary)
                            if len(maxsimirary_word) == 0:
                                if simirary[0] != None:
                                    maxsimirary = float(simirary[0])
                                    maxsimirary_word = result
                            elif simirary[0] and float(simirary[0]) > float(maxsimirary):
                                maxsimirary = simirary[0]
                                maxsimirary_word = result
#                        print('simirary-----------')
#                        print(data[2])
#                        print(maxsimirary_word)
#                        print(maxsimirary)
#                        print('simirary-----------')
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],maxsimirary_word,bool(1))
                        break
                    elif type(results) is str:
                        generateddata = (self.preprocessor.GTPP[0][0],returndata,data[1],results,bool(1))

        return generateddata

    def generateUtterance(self, data, inputType):
        #print ("just before","Topic", data[0], "Property", data[1], "Predicate", data[2])
        #print ("until now", self.preprocessor.GTPP)
        returnstr = []
        """
        発話を生成する

        data      : (A, B, C) の情報が入ったタプル
        inputType : 入力文が 確認(100)/疑問詞質問(200)/YN質問(300)/その他(1000) ... 更新予定
        hasTopic  : Boolean, 作品内の固有表現(例:涼風青葉，など)があるかないか判定
        返値       : String
        """

        generatedString = "うんうん!"

        self.comp = False

        target = data[0]
        Evalu_ax = data[1]
        Evalu = data[2]
        
        # 良さを説明される時
        if inputType == 1000:
            # 全部埋まっているか？
            if self.preprocessor.GTPP[0] and self.preprocessor.GTPP[1] and self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3]:

                if self.rFlg:
                    symData = None
                    
                    # 共感する知識を検索
                    for i in range(3,0,-1):
                        symData = self.generateSympathicWord(i)
                        if symData is None:
                            continue
                        else:
                            break
                
                    # 共感できたか
                    if symData is not None:
                        if i == 3:
                            returnstr.append('%sだしね。' % (symData[0],))
                            returnstr.append('%s、%sだしね。' % (self.preprocessor.GTPP[2][0], symData[0]))
                            returnstr.append('%sだからね。' % (symData[0],))
                            returnstr.append('%s、%sだからね' % (self.preprocessor.GTPP[2][0], symData[0]))
                        elif i == 2:
                            returnstr.append("%sもね。" % (symData[0],))
                            returnstr.append("うんうん，%sもね。" % (symData[0],))
                        elif i == 1:
                            returnstr.append("%sもね。" % (symData[0],))
                            returnstr.append("うんうん，%sもね。" % (symData[0],))
                        self.preprocessor.GTPP[1] = (symData[0], "other")
                        generatedString = choose(returnstr)
                        self.mCounter = 0
                        self.rFlg = False
                        self.comp = True
                        
                # 共感できない場合，直前に共感している場合には，対比を探す。
                if not self.comp or symData is None:
                    rFlg = True
                
                    # 共感できない場合，比較を探す．
                    # 比較できる情報を取得
                    cItem = self.generateConstraction((self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],self.preprocessor.GTPP[3][0]))
                    # 比較できる情報を取得できたら，発話テンプレートを選択して発話を生成
                    if cItem[4] == bool(1):
                        #returnstr.append('たしかに%sだけどさ、%sのほうが%sでいいと思う' % (self.preprocessor.GTPP[3][0],cItem[1],cItem[3]))
                        #returnstr.append('%sの%sは%sはさそうだけど、%sは%sで良くない？' % (self.preprocessor.GTPP[1][0],
                        #                                                                   self.preprocessor.GTPP[2][0],
                        #                                                                   self.preprocessor.GTPP[3][0],
                        #                                                                   cItem[1],
                        #                                                                   cItem[3]))
                        #returnstr.append('たしか、%sの%sは%sだったよねー' % (cItem[1],cItem[2],cItem[3]))
                        returnstr.append('たしかに。そういえば、%sの%sは%sだったよねー' % (cItem[1],cItem[2],cItem[3]))
                        #returnstr.append('%sも好きだよ、だけど%sな%sのほうが好きかなー' % (self.preprocessor.GTPP[1][0],cItem[3],cItem[1]))
                        returnstr.append('うんうん、%sの%sも%sよね' % (cItem[1],cItem[2],cItem[3]))
                        returnstr.append('そうだね、%sの%sも%sよね' % (cItem[1],cItem[2],cItem[3]))
                        generatedString = choose(returnstr)
                        self.preprocessor.GTPP[1] = (cItem[1], "other")
                        self.mCounter = 0
                    # 比較できる情報がない場合，諦めて同意する．
                    else:
                        self.mCounter += 1
                        generatedString = choose(['たしかに．', "そうですね．", "うんうん．", "ええ，そうですね．"])

                
                # topic以外は削除
                self.preprocessor.GTPP[2] = None
                self.preprocessor.GTPP[3] = None
            else:
                # 埋まっていない場合は相槌
                returnstr.append('うん,')
                returnstr.append('はい,')
                returnstr.append('ええ,')
                returnstr.append('うんうん,')
                
                self.mCounter += 1
                
                generatedString = choose(returnstr)

    ######## 2018.5.14 今回は使わない #######

        # 同意を求められた時．
        elif inputType == 100: 
            # もし情報が揃っていれば
            if self.preprocessor.GTPP[0] and self.preprocessor.GTPP[1] and self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3]:
                # 他の predicate を探す
                truedata = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0],'')
                print (truedata)
                # 他にもpredicateがあったら
                if truedata:
                    # 最も入力のpredicateと似ているpredicateを探す
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
                    # 類似度が0.06以上なら
                    if maxsimirary > 0.06:
                        # 同じ単語なら
                        if maxsimirary == 1:
                            # ただの同意
                            returnstr.append('そうだとおもうよ')
                            returnstr.append('あーそうだね')
                            generatedString = choose(returnstr)
                        else:
                            # 否定？？？？ <- する意味ある？
                            returnstr.append('え？%sじゃなっかったっけ' % maxsimirary_word)
                            returnstr.append('%sじゃなくて%sじゃなっかったっけ' % (self.preprocessor.GTPP[3][0],maxsimirary_word))
                            generatedString = choose(returnstr)
                    # 著しく似ていない場合は
                    else:
                        # しらばっくれる
                        generatedString = 'んーどうだっけ、忘れちゃった'
                # 他にpredicateがなかったら
                else:
                    # しらばっくれる
                    generatedString = 'んーどうだっけ、忘れちゃった'
                    
    ########## 2018.5.14 今回は使わない ########
        
        # Y/N の質問だった場合
        elif inputType == 200:
            self.mCounter += 1
            # 現在の発言に情報は全部入っている場合
            if data[0] and data[1] and data[2]:
                # わからないと伝える
                generatedString = 'うーん、わからない，'
            # 現在の会話は少し端折っている場合．
            else:
                # 現在の発話と今までの情報から推察できる場合
                if data[0] and self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3] and self.preprocessor.GTPP[2][0] and self.preprocessor.GTPP[3][0]:
                    # 謝る
                    generatedString = 'ごめん、わからない、'
                # 現在の発話にtopicが入っていなくて，topicが埋まっていない場合
                elif not data[0] and self.preprocessor.GTPP[1]is not None and self.preprocessor.GTPP[1][0] is None:
                    # 質問を返す
                    generatedString = 'だれの？'
                # 現在の発話にtopicが入っていない場合
                elif not data[0]:
                    # propertyとpredicateが埋まっている場合 == 会話の対象がわからないけど，なんか色々言っている場合？
                    if self.preprocessor.GTPP[2] and self.preprocessor.GTPP[3] and self.preprocessor.GTPP[2][0] and self.preprocessor.GTPP[3][0]:
                        # とりあえず同意して，適当にごまかす
                        generatedString = 'あー，たしかに%sだよね、なんでだろう' % self.preprocessor.GTPP[3][0]
                    # 現在の発話の中に属性も入っている場合
                    #elif data[1]:
                        # ハマりそうなpredicateをいれて返す <- これってY/N型の質問の答えになってる？
                        #dbdata = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],data[1],data[2],"")
                        
                        #generatedString = '%sだからじゃない？' % dbdata[0]
                # その他...
                else:
                    # 匙を投げる
                    generatedString = 'わからない'

        # 5W1Hな質問
        elif inputType == 300:
            self.mCounter += 1
            # 無知を晒す
            returnstr.append('うーん，どうなんだろうね')
            returnstr.append('なんでだろう、知らない')
            generatedString = choose(returnstr)


        # マンネリ化している場合
        if self.mCounter > 3:
            if self.preprocessor.GTPP[1] and self.preprocessor.GTPP[2]:
                result = self.accessDB.searchDB(self.preprocessor.GTPP[0][0],self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0], "")
                if type(result) is list:
                    generatedString = "%sの%sは%sですよね" % (self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0], result[0])
                elif type(result) is str:
                    generatedString = "%sの%sは%sですよね" % (self.preprocessor.GTPP[1][0],self.preprocessor.GTPP[2][0], result)
                else:
                    name = choose(self.preprocessor.uniques)
                    generatedString = "%sの話をしませんか？" % (name, )
            else:
                name = choose(self.preprocessor.uniques)
                generatedString = "%sの話をしませんか？" % (name, )
                self.preprocessor.GTPP[1] = (name, "other")
            self.preprocessor.GTPP[2] = None
            self.preprocessor.GTPP[3] = None
            self.mCounter = 0
            
        return (generatedString)
