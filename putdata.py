import json
import os
from AccesDB import AccessToDataBase
directory = os.listdir('dic')
ac = AccessToDataBase()
contents = []
encoded = []
first = None
for i in directory:
    if first is not None:
        print(i)
        with open('dic/' + i) as fh:
            js = json.loads(fh.read())
            contents.append(js)
    else:
        first = i
for l in contents:
    for i in l:
        ac.updateDB((i[0],i[1],i[2],i[3]))
        print(i)
