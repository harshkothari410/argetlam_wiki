#!/usr/bin/python
import urllib2
import urllib
from bs4 import BeautifulSoup
import json
import time
import os

rootPath = os.getcwd() + "/wikiWomensStats/"

dataPath = rootPath + 'data.json'

fullDataPath = '/home/ubuntu/argetlam_wiki_data/data.json'

infoUrl = 'https://en.wikipedia.org/w/index.php?'
infoData = {'title':'','action':'info'}
infoHeaders = { 'User-Agent' : 'Womens edit a thon India' }

cmtitle = "Category:Articles_created_or_expanded_during_Women's_History_Month_(India)_-_2014"
apiUrl = 'https://en.wikipedia.org/w/api.php'
categoryData = {
                  'action' : 'query',
                  'list' : 'categorymembers',
                  'cmtitle' : '',
                  'cmcontinue' : '',
                  'format' : 'json'
                  }

articleEditInfo = {}

def getArticleList(cmtitle):
    articleList = []
    while True:
        categoryData['cmtitle'] = cmtitle
        req = urllib2.Request(apiUrl, headers=infoHeaders, data = urllib.urlencode(categoryData))
        response = json.loads(urllib2.urlopen(req).read())
        
        for article in response['query']['categorymembers']:
            articleList.append(article)
        if 'query-continue' not in response:
            break;
        categoryData['cmcontinue'] = response['query-continue']['categorymembers']['cmcontinue']
    print articleList
    return articleList

def getEditCount(html):
    soup = BeautifulSoup(html)
    return int(soup.findAll('tr',id='mw-pageinfo-edits')[0].findAll('td')[1].text)

def createInfoParams(article):
    infoData['title'] = article
    return urllib.urlencode(infoData)
    
def getArticleEditCount():
    articleList = getArticleList(cmtitle)
    for article in articleList:
        articleTitle = article['title'].replace(' ','_')
        infoParams = createInfoParams(articleTitle)
        req = urllib2.Request(infoUrl, headers=infoHeaders, data = infoParams)
        html = urllib2.urlopen(req).read()
        articleEditInfo[articleTitle] = getEditCount(html)
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
