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
  def updateDB(self,data):
    #do something
    element = self.db.child(data[0]).child(data[1]).child(data[2]).get().val()
    if isinstance(element, str):
        element = [element,data[3]]
    elif isinstance(element, list):
        element.append(data[3])
    else:
        element = data[3]
    self.db.child(data[0]).child(data[1]).child(data[2]).set(element)


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



#ac = AccessToDataBase()
#valll = ac.db.child('NewGame!').get().val()
#print(valll)
#ac.db.child('NEWGAME!').set(valll)
#print('s')
#print(ac.searchDB('NewGame','涼風青葉','髪',''))# $  [eye:blue,small]
#ac.updateDB(('NewGame','八神コウ','耳','緑'))
#ac.getData('test')
