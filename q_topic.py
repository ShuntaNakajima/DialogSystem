#!/usr/bin/env python
# coding:utf-8
from urllib.request import urlopen
from urllib.parse import urlparse
import urllib
import re
import requests
import sys
import lxml.html
from numpy import *

class titleName:

    def __init__(self):
        self.reply_y=str(["うん","ある","はい"])
        self.reply_n=str(["ない","いいえ","ううん"])
        self.state_counter = 0

    def getUtterance(self, i):

        c = self.state_counter
        
        if c == 0:
            self.state_counter = 1
            q_first=["何か好きなアニメとかある？","何かオススメのアニメとかある？"]
            rand=random.choice(q_first)
            return (rand, None)
        
        elif c == 1:
            if i in self.reply_y:
                self.state_counter = 2
                q_first=["タイトルはなんて言うやつ？","なんて名前なの？","何何？気になる！なんてやつ？"]
                rand=random.choice(q_first)
                return (rand, None)
            
            elif i in self.reply_n:
                self.state_counter = 3
                q_first=["じゃあ何か好きなキャラクターを教えてくれる？","何か知ってるキャラクターの名前とか教えてよ"]
                rand=random.choice(q_first)
                return (rand, None)
            else:
                result = self.find_article(i)
                return ("じゃあ"+result+"の話をしよう！"+result+"の好きなところとか聞きたいな！", result)

        else:
            if c == 3:
                #キャラクター名から作品名を聞く
                self.state_counter = 4
                q_first=["ああ、それ何のキャラクターだっけ？"]
                rand=random.choice(q_first)
                return (rand, None)
            else:
                result = self.find_article(i)
                return ("じゃあ"+result+"の話をしよう！"+result+"の好きなところとか聞きたいな！", result)

    def find_article(self, i):
        #https:
        #//qiita.com/yagays/items/e59731b3930252b5f0c4
        par_i=urllib.parse.quote(i)
        print(par_i)
        
        try:
            u = urlopen('https://dic.pixiv.net/a/'+par_i)
            t=u.read()
            print('https://dic.pixiv.net/a/'+par_i)
            a_title=i
        except urllib.error.HTTPError as err:
            #inputされた値の名前の記事がないときはその名前で検索をかける
            print(err.code)
            u = urlopen('https://dic.pixiv.net/search?query='+par_i)
            t=u.read()
            st=str(t)
            a_point=st.find('div class="thumb"')
            print("target point==",a_point)

            if a_point==-1:
                #検索結果がなかったら別のキーワードを問う
                print("うーんごめん、よくわからないや。何かヒントとかない？")
                i = input(">> ")
                result = self.find_article(i)
                a_title=result
                return a_title
            else:
                st_len=len(st)
                print("text length==",st_len)

                par_text=st[a_point-1:st_len]
                char_n=st_len
                while char_n>a_point:
                    char_n=char_n-1
                    a_position='<a href=".*?">'
                    a_url=re.search(a_position,par_text)
                    a_st=a_url.start()
                    a_end=a_url.end()
                    print("url position==",a_st,a_end)
                    a_tag=par_text[a_st+12:a_end-2]
                    break
                art_u = urlopen('https://dic.pixiv.net/a/'+a_tag)
                a_read=str(art_u.read())
                print('https://dic.pixiv.net/a/'+a_tag)
                a_title=urllib.parse.unquote(a_tag)
        print(a_title + "が好きなんだ")
        return a_title
    
if __name__ == "__main__":
    dialog = titleName()
    while True:
        i = input(">> ")
        respond, title = dialog.getUtterance(i)
        print(respond)
        if title is not None:
            print("おわり")
            break
        
