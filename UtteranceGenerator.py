import string
import urllib

class DialogSystem:
    """
    AのBはCという情報を対比という形で使うことで，面白い発話を作る対話システム
    """

    def __init__(self):
        self.theme = 'NewGame'
        self.TABC = ['Topic','A','B','']

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
        if self.TABC[0] and self.TABC[1] and self.TABC[2] and self.TABC[3]:
            pass
        else:
            if hasTopic:
                pass
            else:
                pass
            if inputType == 100:
                generateddata = self.generateConstraction(data)
                generatedString = '%sの%sとかも%sだしね〜' % (generateddata[0],generateddata[1],generateddata[2])
                #net(対比)やがみこうの髪とかも，綺麗だしね
                #generatedString = 'そうですね'
            elif inputType == 200:
                if hasTopic:
                    pass
                else:
                    pass
                if Evaku and Evalu_ax and target:
                    print('確認じゃない？')
                    #全部ある
                    generatedString = 'Error'
                elif Evalu == None and Evalu_ax == None and target == None:
                    print('相槌じゃない？沈黙？')
                    #全部不足
                    generatedString = 'なに？'
                elif Evalu == None and Evalu_ax and target:
                    #AとBはある
                    generatedString = 'うん，'
                elif Evalu == None:
                    if Evalu_ax == None:
                        #Aだけがある 花子？ -> よしこ (theme=アホガール,間違った性別=女,主人公)
                        generatedString = 'うん，'
                    else:
                        #Bだけがある
                        generatedString = 'うん，'
                elif Evalu_ax == None and target == None:
                    generatedString = 'うん，'
                    #Cだけがある
                elif Evalu_ax:
                    generatedString = 'うん，'
                    #CとBはある
                elif target:
                    generatedString = 'うん，'
                    #CとAはある
                else:
                    generatedString = ''
                    print('what happend?')
            elif inputType == 300:
                generatedString = 'わかりません'
                #net
            elif inputType == 1000:
                if target == None:
                    pass
                generatedString = 'うん，'
            return (generatedString)
