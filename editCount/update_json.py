#!/usr/bin/python
import urllib2
import urllib
from bs4 import BeautifulSoup
import json
import time
import os

dataPath = '~/wikiWomensStats/data.json'

fullDataPath = '/home/user/wikiWomensStats/data.json'

infoUrl = 'https://en.wikipedia.org/w/index.php?title=Vimla_Varma&action=info'
infoData = {'title':'','action':'info'}
infoHeaders = { 'User-Agent' : 'Womens edit a thon India' }

articleList = ['Vimla_Varma','Rani_Chithraleksha_Bhosale','Kim_Gangte','Satwinder_Kaur_Dhaliwal','Usha_Meena',"Beatrix_D'Souza"]
articleList += ['Geeta_Mukherjee','Bhagwati_Devi','Omvati_Devi','Sukhda_Misra','Reena_Choudhary','Krishna_Bose','Lakshmi_Panabaka']
articleList += ['Rama_Devi_(Muzaffarpur)','Mala_Rajya_Laxmi_Shah','Rajkumari_Ratna_Singh','Alka_Nath','Ketki_Devi_Singh','Maharani_Divya_Singh']
articleList += ['Purnima_Verma','Gundu_Sudha_Rani','Sandhya_Bauri','Malti_Devi','Bhavna_Kardam_Dave','Nisha_Chaudhary','Kailasho_Devi']

articleEditInfo = {}

def getEditCount(html):
    soup = BeautifulSoup(html)
    return int(soup.findAll('tr',id='mw-pageinfo-edits')[0].findAll('td')[1].text)

def createInfoParams(article):
    infoData['title'] = article
    return urllib.urlencode(infoData)
    
def getArticleEditCount():
    for article in articleList:
        infoParams = createInfoParams(article)
        req = urllib2.Request(infoUrl, headers=infoHeaders, data = infoParams)
        html = urllib2.urlopen(req).read()
        print article, 'page received'
        articleEditInfo[article] = getEditCount(html)
    return articleEditInfo

def writeJson():
    temp = getArticleEditCount()
    with open(fullDataPath,'a') as f:
        temp['timestamp'] = time.time() 
        f.write(json.dumps(temp)+'\n')
    f.close() 

def readJson():
    pointer = -2
    with open(fullDataPath,'r') as f:
        while f.read(1) != '\n':
            f.seek(pointer,2)
            pointer -= 1
        latest = f.readline()
    f.close()
    return json.loads(latest)

if __name__ == "__main__":
    writeJson()
