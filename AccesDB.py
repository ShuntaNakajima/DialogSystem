import time
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
    pass
  def getData(self,genre):
     #1日以内にキャッシュされてたら再び取らない．
    data = self.db.child(genre).get()
    if data.val() == None:
        self.updateDB(genre)
    else:
        last_update = self.db.child(genre).child('last-update').get()
        if int(last_update) + 86400 <  time.time():
            self.updateDB(genre)
        else:
            print('キャッシュが残ってますよ．（%s）秒前' % (time.time() - int(last_update)))

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
    #  print(searchDB(NewGame!,'',eye,blue)) $  [eye:aoba_suzukaze,....] 所得に失敗した時 $ [eye:None]
    #  print(searchDB(NewGame!,'kou_yagami','','')) $  [eye:[blue,small],]
    #  print(searchDB('','aoba_suzukaze',eye,blue)) $  []
    #  print(searchDB('NewGame!','','',blue)) $  []
    #  print(searchDB('NewGame!','aoba_suzukaze','eye',blue)) $  [eye:blue,small]
    #  print(searchDB('NewGame!','aoba_suzukaze','eye',red)) $  [eye:blue]
    if genre == None:
        return []
    if topic == None:
        if proper and predicate:
            recivedData = self.db.child(theme).order_by_child(proper).get()
            if predicate in recivedData.val():  
                for i in recivedData.val():
                    valList.append(i)
                result = valList
            else:
                result = valList
        else:
            return []
    else:
        if proper and predicate:
            pass
        elif proper:
            result = self.db.child(genre).child(topic).child(proper).get()
        else:
            result = self.db.child(genre).child(topic).get()
            for i in result.key():
                print(result.val())
                if predicate:
                    for j in result[i].val():
                        if j.val() == predicate:
                            passok = bool(1)
            if predicate:
                if passok:
                    return result
                else:
                    return []
            else:
                return result.val()

    print(result.val())


ac = AccessToDataBase()
print(ac.searchDB('NewGame','涼風青葉','',''))# $  [eye:blue,small]

#ac.getData('test')
