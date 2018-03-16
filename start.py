from UtteranceGenerator import DialogSystem

dia = DialogSystem()

def start():
    print ('A')
    A = input("")
    print ('B')
    B = input("")
    print ('C')
    C = input("")
    print ('inputType')
    inputtype = input("")
    print ('hasTopic')
    hastopic = input("")
    print ('topic')
    dia.theme = input("")
    data = [A,B,C]
    result = dia.generateUtterance(data,int(inputtype),bool(hastopic))
    print(result)
if __name__ == '__main__':
    start()
