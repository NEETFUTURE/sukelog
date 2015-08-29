# -*-coding: utf-8 -*-

import requests
from urllib import request
from os import path
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import sys

SUKE ="http://fox.2ch.net/test/read.cgi/poverty/1438690970/"
threads=[]

exts=(".jpg",".png",".bmp",".gif",".jpeg",
      ".JPG",".PNG",".BMP",".GIF",".JPEG")


class thread(object):
    def __init__(self,url):
        self.url = url
        self.body = get_thread(url)
        self.res = []
        self.title = extrc_txt(self.body)
        self.leng = 0
        self.gazo_index = 0

    def update(self):
        body = get_thread(self.url)
        if len(self.body) > len(body):
            print("%d > %d"%(len(self.body),len(body)))
            return False
        print("thread is alive.")
        soup = BeautifulSoup(self.body,"lxml")
        newres = soup.find_all("a",text=re.compile("http"))
        print("newles is %d"%(len(newres)))
        sa =  len(newres)-self.leng
        if sa == 0:
            return False
        self.res = newres
        for i in range(sa):
            uRl = self.res[i+self.leng].string
            print("uRl = %s"%(uRl))
            if isImage(uRl):
                download(uRl,self.gazo_index)
                self.gazo_index+=1
        self.leng = len(newres)
        return True


def isImage(stri):
    ext = path.splitext(stri)[-1]
    for i in exts:
        if i == ext:
            return True
    return False

def download(url,n):
    img = request.urlopen(url)
    with open("%05d_%s"%(n,path.basename(url).strip()), 'wb') as ff:
        ff.write(img.read())
    print("%05d_%sをゲット!"%(n,path.basename(url)))

def get_thread(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    return r.text

def extrc_txt(text):
    soup = BeautifulSoup(text,"lxml")
    r = soup.find("h1")
    print(r)

if __name__ == "__main__":
    print("Hello world")

    thr = thread("http://anago.2ch.net/test/read.cgi/jan/1410061993/")
    print(thr.update())

