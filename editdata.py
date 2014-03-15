#!/usr/bin/python
import urllib2
import urllib
from bs4 import BeautifulSoup
import json
import time
import os
import collections

# rootPath = os.getcwd() + "/wikiWomensStats/"

# dataPath = rootPath + 'data.json'

# fullDataPath = rootPath + 'data.json'

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
    #print articleList
    return articleList

def createInfoParams(article):
    infoData['title'] = article
    return urllib.urlencode(infoData)
    
import requests
user = []
totalEdit = 0
ip_user = []
user_edit = 0
ip_user_edit = 0
articles = {}
general = {}

articleList = getArticleList(cmtitle)
#print articleList

print "------Articles wise Edit Count-------"

for article in articleList:
	articleTitle = article['title'].replace(' ','_')
	articleId = article['pageid']
	r = requests.get('http://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&rvprop=timestamp%7Cuser%7Ccomment&rvlimit=500&rvstart=20140301000000&rvdir=newer&titles='+articleTitle)

	a = r.json()
	# print a['query']['pages'][str(articleId)]['revisions']
	# print articleId
	# print a['query'][]
	final = a['query']['pages'][str(articleId)]['revisions']

	print article['title'] + '\t\t' + str(len(final))
	articles[article['title']] = len(final)
	for item in final:
		if item.has_key('anon'):
			ip_user.append(item['user'])
		else:
			user.append(item['user'])


user_edit = len(user)
ip_user_edit = len(ip_user)
final_user = set(user)
final_ip_user = set(ip_user)

general['totalEdit'] = user_edit + ip_user_edit
general['userEdit'] = user_edit
general['ipEdit'] = ip_user_edit
general['userCount'] = len(final_user)
general['ipCount'] = len(final_ip_user)

#print final_user
#print len(final_user)

print "Results\n"
print "Total Edit Count : ",user_edit + ip_user_edit
print "Total Edit by User : ",user_edit
print "Total Edits from IP : ",ip_user_edit
print "User Count : ",len(final_user)
print "Total distinct IP count : ",len(final_ip_user)

counter=collections.Counter(user)
#print counter

countrip = collections.Counter(ip_user)

json1 = open('wikiwomanstats/useredit.json','w')
josn2 = open('wikiwomanstats/articledit.json','w')
json3 = open('wikiwomanstats/generalstats.json','w')
completeEdit = {'user':counter,'ip':countrip}
completeEdit = json.dumps(completeEdit)


json1.write(completeEdit)
josn2.write(json.dumps(articles))
json3.write(json.dumps(general))



print "\n ------User List with Edit count------"

for users,edit in counter.iteritems():
	print users + '\t\t' + str(edit)

print "\n ------Ip User List with Edit count------"

for users,edit in countrip.iteritems():
	print str(users) + '\t\t' + str(edit)






