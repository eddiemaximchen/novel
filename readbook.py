import json
from gtts import gTTS
import os
#need to install gtts and mpg123
#need to run downloadtxt.py first
def readBook():
    # receive selection
    print('Book to read:')
    book=input()
     # get readlist
    with open("./novels/bookList.json", "r", encoding="utf-8") as file:
             strJson = file.read()
    readList = json.loads(strJson)
     # get book content
    filename=""
    for i in range(len(readList)):
         if(readList[i]['title']==book):
            filename = './novels/'+readList[i]['title']+'_'+readList[i]['num']+'.txt'
            content = open(filename, "r", encoding="utf-8")
            read = True
            while read:
                line=content.read(100)
                tts=gTTS(text=line,lang='zh')
                mp3file='test.mp3'
                tts.save(mp3file)
                os.system('mpg123 ' +'test.mp3')
                if not content:
                    print("End of Book")
                    read = False
if __name__ == "__main__":
    readBook()
