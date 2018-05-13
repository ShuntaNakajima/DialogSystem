# -*- coding: utf-8 -*-
import json
import os
from AccesDB import AccessToDataBase
directory = os.listdir('dic')
ac = AccessToDataBase()
'''contents = []
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
        print(i)'''
print('なんの作品？')
gen = input()
print('誰？')
who = input()
print('何？')
what = input()
print('どんなかんじ？')
c = input()
ac.updateDB((gen,who,what,c))
while True:
    if who:
        if what:
            print('どんなかんじ？')
            c = input(gen + '->' + who + '->' + what)
            if c == 'g':
                what = ''
            else:
                ac.updateDB((gen,who,what,c))
        else:
            print('どんなかんじ？')
            what = input(gen + '->' + who)
            if what == 'g':
                who = ''
    else:
        print('誰？')
        who = input()
