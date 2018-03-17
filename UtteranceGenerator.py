import string
import urllib
import yaml

class DialogSystem:
    """
    AのBはCという情報を対比という形で使うことで，面白い発話を作る対話システム
    """

    def __init__(self):
        self.theme = 'NewGame'
        self.TABC = ['Topic','A','B','C']
        #with open("resource/ahalist.yml") as file:
        #    self.ahalist = yaml.load(file)
        #print (self.ahalist[0])

    def searchData(self,text):
        pass
    def generateConstraction(self, data):
        """
        発話に使用するための対比を生成する

        返値 : (A, B, C) の情報が入ったタプル
        """
        if data == ['青葉','髪','きれい']:
            generateddata = ['八神公','髪','きれい']
        else:
            generateddata = data
        print ('GeneratedConstraction!:%s,%s,%s' % (generateddata[0],generateddata[1],generateddata[2]))
        return generateddata

    def generateUtterance(self, data, inputType, hasTopic):
        print ("A:" + data[0] + ",B:" + data[1] + ",C:" + data[2])
        print (self.TABC)
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
            if self.TABC[0] and self.TABC[1] and self.TABC[2] and self.TABC[3]:
                if data[0] or data[1] or data[2]:
                    contractionItem = self.generateConstraction((self.TABC[1],self.TABC[2],self.TABC[3]))
                    generatedString = 'あー，%sの%sが%sみたいにね' % (contractionItem[0],contractionItem[1],contractionItem[2])
                else:
                    #ゼブンブない？
                    pass
            else:
                generatedString = 'うん,'
        else:
            if inputType == 100:
                generatedString = 'あーそうだと思うよ'
                #net
            elif inputType == 200:
                generatedString = 'なんでだっけ，'
                #net
                #generateConstraction((self.TABC[1],self.TABC[2],self.TABC[3]))
            elif inputType == 300:
                generatedString = 'うーん，どうなんだろうね...'
        return (generatedString)
