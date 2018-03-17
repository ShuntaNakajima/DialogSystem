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
  def updateDB(self,theme):
      #do something

  def getData(self,theme):
    data = self.db.child(theme).get()
    if data.val() == None:
        self.updateDB(theme)
    else:
        last_update = self.db.child(theme).child('last-update').get()
        if int(last_update) + 86400 <  time.time():
            self.updateDB(theme)
        else:
            print('キャッシュが残ってますよ．（%s）秒前' % (time.time() - int(last_update)


ac = AccessToDataBase()
ac.getData('test')
