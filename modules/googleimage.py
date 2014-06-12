import urllib2
import simplejson
import urllib
import cStringIO
import json as m_json
import modules
import Image
import os

bot=None

def google(terms): # !google <search term>
	fetcher = urllib2.build_opener()
	searchTerm = terms.replace(' ','+')
	startIndex = 0
	searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(startIndex)
	print searchUrl
	f = fetcher.open(searchUrl)
	a=simplejson.load(f)
	imageUrl = a['responseData']['results'][0]['unescapedUrl']
	print imageUrl
	file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
	try:
		img = Image.open(file)
	except IOError:
		return None
	imageUrl=imageUrl.replace(':/','')
	imageUrl=imageUrl.replace('/','')
	saveurl=os.path.join('downloads',imageUrl)
	img.save(saveurl)
	print saveurl
	return saveurl
	
	
	
def AI(jid,query,querer,group):
	query=query[len("image "):]
	result=google(query)
	if result:
		modules.photosender.photo_queue(jid,result)
	else:
		modules.sender.message_queue(jid,"unable to fetch that")

def onMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	if messageContent.lower().startswith("image "):
		AI(jid,messageContent,pushName,None)
		
def onGroupMessageReceived(messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
	if messageContent.lower().startswith("image "):
		AI(jid,messageContent,pushName,msgauthor)

def setup(parent):
	parent.signalsInterface.registerListener("message_received", onMessageReceived)
	parent.signalsInterface.registerListener("group_messageReceived", onGroupMessageReceived)
	global bot
	bot=parent
