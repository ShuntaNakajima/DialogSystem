from datetime import datetime
import os

class writeLog:
    def __init__(self,option=None):
        if option:
            if os.path.isdir("./logs-%s" % option) == False:
                os.mkdir("./logs-%s" % option)
            self.filename = 'logs-%s/' % option + datetime.now().strftime("%Y-%m-%d-%H-%M") + '.text'
        else:
            if os.path.isdir("./logs") == False:
                os.mkdir("./logs")
            self.filename = 'logs/' + datetime.now().strftime("%Y-%m-%d-%H-%M") + '.text'
        print('logfile : ' + self.filename)
    def writeLog(self,mode,text):
        text = text + "\n"
        with open(self.filename,'a') as f:
            time = datetime.now().strftime("%H:%M:%S")
            if mode == 'system':
                f.write(time + ' : system --> ' + text)
            else:
                f.write(time + ' : user   --> ' + text)
