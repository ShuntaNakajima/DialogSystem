from UtteranceGenerator import DialogSystem

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
    dia.TABC = [dia.theme,AA,BB,CC]
    data = (A,B,C)
    result = dia.generateUtterance(data,int(inputtype),bool(hastopic))
    print(result)
if __name__ == '__main__':
    start()
