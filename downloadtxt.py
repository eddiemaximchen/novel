from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import json
import re
import os

# 建立儲存書本的資料夾，不存在就新增
folderPath = 'novels'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
bookList=[]
#收集書本資訊
def getBooksData():
    url = 'https://www.gutenberg.org/browse/languages/zh'
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'html.parser')
    regex01 = "[^a-zA-Z0-9\W]+"
    prevTitle=""
    for a in bs.select('div.pgdbbylanguage li.pgdbetext a'):
        if a.has_attr('href'):
            # 取得書名
            title = a.get_text()
            title=re.match(regex01,title)
            # 取得書籍編號
            regex02 = "[\d]+"
            match = re.search(regex02, a['href'])
            num = match[0]
            
            # 將[書名,書籍編號,下載連結]放入 list 中
            if title != None:
                bookList.append({
                    'title':title[0],
                    'num':num,
                    'download':'https://www.gutenberg.org/files/%s'%num+'/'+'%s'%num+'-0.txt'
                })

def saveJson():
    # 寫入 書籍資訊 in json 檔
    with open(f"{folderPath}/bookList.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(bookList, ensure_ascii=False, indent=4))

def saveTxt():
    #下載資料
    for i in range(len(bookList)):
        print(bookList[i]['title'])
        html1 = urlopen(bookList[i]['download'])
        bs1 = BeautifulSoup(html1.read(),'html.parser')
        strJson=bs1.get_text()
        #去掉英文
        strJson = re.sub(r"[^\u4e00-\u9fa5]+", '', strJson)      
 
        # 決定 txt 的檔案名稱
        fileName = f"{bookList[i]['title']}_{bookList[i]['num']}.txt"
 
        # 將小說內容存到 novels 中
        with open(f"{folderPath}/{fileName}", "w", encoding="utf-8") as file:
            file.write(strJson)
  
if __name__ == "__main__":
    getBooksData()
    saveJson()
    saveTxt()
