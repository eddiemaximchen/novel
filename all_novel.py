from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
def getNovel(articleNum):
    
    url='https://tw.hjwzw.com/Book/Chapter/%s'%articleNum
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    title=bs.find("head").title.get_text()
    length=title.find('/')  #求得書名的長度
    #去掉非文字部份
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

    regex01=r'\w{%s}(?=\/)'%length
    title=re.match(regex01,title)
    str='<h1>%s</h1>'%title[0]
    #找到div的dom
    books=bs.find('div',{'id':'tbchapterlist'})
    #把網址改成絕對路徑
    for a in books.select('a'):
        a['href']="https://tw.hjwzw.com"+a['href']
    #找出所有章節
    for book in books:
        str=str+'%s'%book
    #放在子資料夾novels 如果沒有就新增    
    folderPath = os.path.join(os.getcwd(), 'novels')
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    path='./novels/%s.html'%title[0]
    fileobj =open(path, 'wt',encoding='UTF-8')
    print(str,file=fileobj)
    fileobj.close()

html = urlopen('https://tw.hjwzw.com/Channel/all')
bs = BeautifulSoup(html.read(),'html.parser')
links=bs.find_all('a')
for link in links:
    regex01=r'/Book/\d+'
    url=re.match(regex01,link.attrs['href'])
    if url:
        chapters=url.group().split('/Book/')
        chapters=chapters[1].split()
        for chapter in chapters:
            getNovel(chapter)
