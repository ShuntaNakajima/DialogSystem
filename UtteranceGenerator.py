import string
import urllib

class DialogSystem:
    """
    AのBはCという情報を対比という形で使うことで，面白い発話を作る対話システム
    """

    def __init__(self):
        self.theme = 'NewGame'
    def searchData(self,text):
        pass
    def generateConstraction(self, data):
        """
        発話に使用するための対比を生成する

        返値 : (A, B, C) の情報が入ったタプル
        """
        return data

    def generateUtterance(self, data, inputType, hasTopic):
        print ("A:" + data[0] + ",B:" + data[1] + ",C:" + data[2])
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
        if hasTopic:
            pass
        else:
            pass

        if inputType == 100:
            generatedString = 'そうですね'
        elif inputType == 200:
            if hasTopic:
                pass
            else:
                pass
            generatedString = ''
        elif inputType == 300:
            generatedString = 'わかりません'
        elif inputType == 400:
            if target == None:
                pass
            generatedString = '私も%sの%sは%sだと思います！' % (target,Evalu_ax,Evalu)
        return (generatedString)
