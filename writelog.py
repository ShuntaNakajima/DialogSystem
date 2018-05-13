from datetime import datetime

class writeLog:
    def __init__(self):
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
