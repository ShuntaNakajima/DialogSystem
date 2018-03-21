import pyrebase

class AccessToDataBase:
    #ジャンル トピック プロパティー プレディケイと
  def __init__(self):
    self.config = {
          "apiKey": "AIzaSyCA9NmzoNn5wC63wzdKuwCwhrPL4Ccuzew",
          "authDomain": "dialogsystem-7767f.firebaseapp.com",
          "databaseURL": "https://dialogsystem-7767f.firebaseio.com",
          "storageBucket": ""
          }
    self.firebase = pyrebase.initialize_app(self.config)
    self.db = self.firebase.database()
  def updateDB(self,genre):
    #do something
    self.db.child("NewGame").child("八神コウ").child('目').set(('黄色','小さい'))
    pass

  def searchDB(self,genre,topic,proper,predicate):
    #DBを検索する.ジャンルは必須，
    #トピックがない場合には，プロパティーとプレディケイとが必要
    #ジャンルとトピックだけだと所得したデータの全てを返す
    #全てが埋まっていたら，確認用に使用可能
    #DB構成図
    # root - NewGame! |-aoba_suzukaze |-eye |-blue
    #      |          |               |     |
    #      |          |               |     |-small
    #      |          |               |
    #      |          |               |-hear |- long
    #      |          |               .      |- twin
    #      |          |               .      |- blue
    #      |          |               .
    #      |          |
    #      |          |-kou_yagami ---|-eye |-yellow
    #      |                          |     |
    #      |                          |     |-small
    #      |                          |
    #      |                          |-hear |- long
    #      .                          .      |- strate
    #      .                          .      |- gold
    #      .                          .
    #
    #  print(searchDB(NewGame!,aoba_suzukaze,eye,'')) $  [eye:blue,small]
    #  print(searchDB(NewGame!,'',eye,blue)) $  [aoba_suzukaze,hihumi,....] 所得に失敗した時 $ [eye:None]
    #  print(searchDB(NewGame!,'kou_yagami','','')) $  [eye:[blue,small],]
    #  print(searchDB('','aoba_suzukaze',eye,blue)) $  []
    #  print(searchDB('NewGame!','','',blue)) $  []
    #  print(searchDB('NewGame!','aoba_suzukaze','eye',blue)) $  [eye:blue,small]
    #  print(searchDB('NewGame!','aoba_suzukaze','eye',red)) $  [eye:blue]
    if not genre:
        return []
    if not topic:
        result = []
        if proper and predicate:
            recivedData = self.db.child(genre).get()
            for i in recivedData.val():
                for j in recivedData.val()[i].keys():
                    if j == proper:
                        if predicate in recivedData.val()[i][j]:
                            result.append(i)
            return result
        else:
            return []
    else:
        trueResult = []
        if predicate and not proper:
            result = self.db.child(genre).child(topic).get()
            for i in result.val():
                for j in result.val()[i]:
                    if j == predicate:
                        trueResult.append(i)
            return trueResult
        else:
            result = self.db.child(genre).child(topic).child(proper).get()
            for i in result.val():
                trueResult.append(i)
            return trueResult



ac = AccessToDataBase()
print(ac.searchDB('NewGame','涼風青葉','髪',''))# $  [eye:blue,small]
#ac.updateDB('a')
#ac.getData('test')
