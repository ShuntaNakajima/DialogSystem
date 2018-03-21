from UtteranceGenerator import DialogSystem
from jwn_corpusreader import JapaneseWordNetCorpusReader
dia = DialogSystem()

def start():
    print ('A')
    A = input("")
    print ('B')
    B = input("")
    print ('C')
    C = input("")
    print ('AA')
    AA = input("")
    print ('BB')
    BB = input("")
    print ('CC')
    CC = input("")
    print ('inputType')
    inputtype = input("")
    print ('hasTopic')
    hastopic = input("")
    print ('topic')
    dia.theme = input("")
    dia.theme = 'NewGame'
    dia.TABC = ["NewGame","八神コウ","髪","短い"]
    data = ("八神コウ","髪","黄色")
    #result = dia.generateUtterance(data,int(inputtype),bool(hastopic))
    result = dia.generateUtterance(data,1000,bool(0))
    print(result)

if __name__ == '__main__':
    #start()
    dia.preprocessor.GTPP[0] = ['NewGame',None]
    dia.dialog_state = "a"
    #dia.preprocessor
    dia.main('八神コウの髪は短い')
