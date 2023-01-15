from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

def getNovel(articleNum):
    
    url='https://tw.hjwzw.com/Book/Chapter/%s'%articleNum
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    title=bs.find("head").title.get_text()
    #求得書名的長度
    length=title.find('/')  
    #表達式無法過濾去掉非文字部份 所以先去掉
    if '，'  in title:
        title=title.replace('，','')
        length=length-1

    if '：'  in title:
        title=title.replace('：','')
        length=length-1

    if '!'  in title:
        title=title.replace('!','')
        length=length-1

    if '?'  in title:
        title=title.replace('?','')
        length=length-1
    #去掉書名後的文字 動態給表達式長度
    regex01=r'\w{%s}(?=\/)'%length
    title=re.match(regex01,title)
    #內文標題是書名
    str='<h1>%s</h1>'%title[0]
    #所有的章節 
    for child in bs.find('div',{'id':'tbchapterlist'}).children:
        str=str+'%s'%child
    #放在子資料夾novels 如果沒有就新增    
    folderPath = os.path.join(os.getcwd(), 'novels')
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    #寫入檔案 檔名是書名
    path='./novels/%s.html'%title[0]
    fileobj =open(path, 'wt',encoding='UTF-8')
    print(str,file=fileobj)
    fileobj.close()
#鬥破蒼穹
getNovel('1642')