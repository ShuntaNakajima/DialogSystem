#!/usr/bin/env python
# coding:utf-8
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib
import re
import requests
import sys
import lxml.html
class UrlName:
    def find_url(self,i):
        #https:
        #//qiita.com/yagays/items/e59731b3930252b5f0c4
        par_i=urllib.parse.quote(i)
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
        while char_n>point:
            char_n=char_n-1

            url_st='<a href="'
            uspoint=par_text.find(url_st)
            url_end='"><img'
            uepoint=par_text.find(url_end)
            print("url position==",uspoint,uepoint)
            article=par_text[uspoint+12:uepoint]
            print(article)
            if uspoint !=-1:
                break
        art_u = urlopen('https://dic.pixiv.net/a/'+article)
        a_read=str(art_u.read())
        print('https://dic.pixiv.net/a/'+article)
        a_title=urllib.parse.unquote(article)
        return a_title
