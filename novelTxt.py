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
        title=title.replace('：','')
        length=length-1        
    #去掉書名後的文字 動態給表達式長度
    regex01=r'\w{%s}(?=\/)'%length
    title=re.match(regex01,title)
    #內文標題是書名
    str='<h1>%s</h1>'%title[0]
    chapters=[]
    #找到div的dom
    books=bs.find('div',{'id':'tbchapterlist'})
    #把網址改成絕對路徑
    for a in books.select('a'):
        a['href']="https://tw.hjwzw.com"+a['href']
        #準備把所有章節變成文字檔
        chapters.append(a['href'])
    #找出所有章節
    for book in books:
        str=str+'%s'%book
    #找出全文
    textData=[]
    for chapter in chapters:
        link = urlopen(chapter)
        text=BeautifulSoup(link.read(),'html.parser').get_text()
        textData.append(text)
    #放在子資料夾novels 如果沒有就新增    
    folderPath = os.path.join(os.getcwd(), 'novels')
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    #寫入章節 檔名是書名
    path='./novels/%s.txt'%title[0]
    fileobj =open(path, 'wt',encoding='UTF-8')
    print(text,file=fileobj)
    #寫入全文 檔名是書名
    with open('./novels/%s.txt,'w',encodjng='utf-8')
        file.write('\n'.join(textData))
    fileobj.close()
if __name__=="__main__":  
#鬥破蒼穹
    getNovel('1642')
