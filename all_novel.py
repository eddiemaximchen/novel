from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
#鬥破蒼穹目錄
def getNovel(articleNum):
    
    url='https://tw.hjwzw.com/Book/Chapter/%s'%articleNum
    html = urlopen(url)
    print(url)
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
    str1='<h1>%s</h1>'%title[0]
    #所有的章節
    for child in bs.find('div',{'id':'tbchapterlist'}).children:
        str1=str1+'%s'%child
    #放在子資料夾novels 如果沒有就新增 
    folderPath = os.path.join(os.getcwd(), 'novels')
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    #寫入檔案 檔名是書名
    path='./novels/%s.html'%title[0]
    fileobj =open(path, 'wt',encoding='UTF-8')
    fileobj.close()

html = urlopen('https://tw.hjwzw.com/Channel/all')
bs = BeautifulSoup(html.read(),'html.parser')
links=bs.find_all('a')
for link in links:      #只需要擷取連結中數字的部份
    regex01=r'/Book/\d+'
    url=re.match(regex01,link.attrs['href'])
    if url:
        chapters=url.group().split('/Book/')
        chapters=chapters[1].split()
        for chapter in chapters:
            getNovel(str(chapter))
print ('done')
