
# coding: utf-8

# In[43]:

import requests
import os
import io
from bs4 import BeautifulSoup
import json

class Question:
    def __init__(self,id,question,options,ans,exp):
        self.id=id
        self.question=question
        self.options=options
        self.ans=ans
        #self.exp=exp
    def writetofile(self,topic,subtopic,Quest):
        mf=open('bix.json',"a")
        data={}
        data[topic]={}
        data[topic][subtopic]=[]
        for i in Quest:
            data[topic][subtopic].append(i.__dict__)
            
        json.dump(data,mf)
        mf.close()
        
site="http://www.indiabix.com"
counter=0
curls=["http://www.indiabix.com/aptitude/questions-and-answers/",
      ]
for zx in curls:
    subpage=zx
    page=requests.get(subpage)
    soup=BeautifulSoup(page.content,'html.parser')
    content=soup.findAll(class_='div-topics-index')
    mainurls=[]
    tx=content[0].select('li')
    topic=zx[24:].partition("/")[0].title()
    for i in tx:
        x=i.select('a')[0]['href']
        #print(x)
        mainurls.append(x)
    tx=content[1].select('li')
    for i in tx:
        x=i.select('a')[0]['href']
        mainurls.append(x)
    
    for murl in mainurls:
        cururl=murl
        subtopic=murl
        myques=[]
        page=requests.get(site+cururl)
        soup=BeautifulSoup(page.content,'html.parser')
        foot=soup.findAll(class_='mx-pager mx-lpad-25')
        i=0
        #print(cururl)
        vb=foot[0].select('a')
        #print(vb)
        ux=set()
        ux.add(page.url)
        for i in vb:
            bc=i['href']
            ux.add(site+bc)
            
        for i in ux:
            #print(i)
            text=soup.findAll(class_='bix-tbl-container')
            l=len(text)
            i=0;
            while(i<l):
                data=text[i].select('p')[0].get_text()
                #print (data)
                question=data
                j=1;
                op=text[i].findAll(class_='bix-td-option')
                options=[]
                while(j<len(op)):
                    #print(op[j].get_text())
                    options.append((op[j].get_text()))
                    j+=2
                    #print("")
                ans=text[i].find(class_='jq-hdnakqb mx-bold').get_text()
                exp=str(text[i].find(class_='bix-ans-description').get_text().split())
                #print(exp)  
                obj=Question(counter,question,options,ans,exp)
                myques.append(obj)
                i+=1
                counter+=1
        cururl=site+foot[0].select('a')[len(foot[0].select('a'))-1]['href']
        obj.writetofile(topic,subtopic.split('/')[2].title().replace('-',' '),myques)
        #print("1")
        #print(counter)

