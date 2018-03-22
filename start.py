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
    dia.theme = 'NEWGAME!'
    dia.TABC = ["NEWGAME!","八神コウ","髪","短い"]
    data = ("八神コウ","髪","黄色")
    #result = dia.generateUtterance(data,int(inputtype),bool(hastopic))
    result = dia.generateUtterance(data,1000,bool(0))
    print(result)

if __name__ == '__main__':
    dia.preprocessor.GTPP[0] = ['NEWGAME!',None]
    dia.dialog_state = "a"
    #dia.preprocessor

    dia.url = 'http://192.168.11.14:8080'
    dia.start()
        

    #通信テスト
    dia.output('こんにちは、てるみんです。', url='http://192.168.11.14:8080')


    print("======八神コウの髪は短い======")
    print(dia.main('八神コウの髪は短い'))

    print("======八神コウの髪は短い======")
    print(dia.main('八神コウの髪は短い'))

    print("======八神コウの髪がさー======")
    print(dia.main('八神コウの髪がさー'))

    print("======八神コウって短いよね======")
    print(dia.main('八神コウって短いよね'))

    print("======八神コウってさー======")
    print(dia.main('八神コウってさー'))

    print("======髪の毛がさー======")
    print(dia.main('髪の毛がさー'))

    print("======短いよねー======")
    print(dia.main('短いよねー'))
