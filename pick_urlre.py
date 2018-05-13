#!/usr/bin/env python
# coding:utf-8
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib
import re
import requests
import sys
import lxml.html
from numpy.random import *
from AccesDB import AccessToDataBase as AC
class UrlName:
    def find_url(self,i):
        #https:
        #//qiita.com/yagays/items/e59731b3930252b5f0c4
        par_i=urllib.parse.quote(i)
        par_i=par_i.replace('%20','')
        print(par_i)

        u = urlopen('https://dic.pixiv.net/a/'+par_i)
        print(u)
        t=u.read()
        asc=t[:1024].decode('ascii',errors='replace')
        char=re.search(r'charset=[''"''¥'']?([¥w-]+)',asc)
        if char:
            enc=char.group(1)
        else:
            enc='utf-8'
        #print(enc)
        st=str(t)

        tag = str(u'兄弟記事'.encode())
        n=1
        tlen=len(tag)
        txt=tag[n+1:tlen-1]
        #print(txt)

        point = st.find(txt)
        #print("target point==",point)

        st_len=len(st)
        #print("text length==",st_len)

        par_text=st[point-1:st_len]
        char_n=st_len
        url_st='<a href="'
        url_end='"><img'
        texlist = par_text.split(url_st)
        j = []
        for i in texlist:
            if url_end in i:
                j.append(i)
        n = []
        for i in j:
            tex = i.split(url_st)
            spli = tex[0].split(url_end)
            if '/a/' in spli[0]:
                n.append(spli[0])
        j = []

        ac = AC()
        for i in ac.getTopiclist('君の名は。'):
            par_i=urllib.parse.quote(i)
            par_i=par_i.replace('%20','')
            for c in n:
                if par_i in c:
                    j.append(par_i)
        print(j)
        def choose(mylist):
            num = randint(0,len(mylist) - 1)
            return mylist[num]
        article = choose(j)
        art_u = urlopen('https://dic.pixiv.net/a/'+article)
        a_read=str(art_u.read())
        print('https://dic.pixiv.net/a/'+article)
        a_title=urllib.parse.unquote(article)
        for i in ac.getTopiclist('君の名は。'):
            par_i=i.replace(' ','')
            if a_title == par_i:
                return i
        return a_title
