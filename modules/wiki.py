from BeautifulSoup import BeautifulSoup
import urllib2
import modules

import requests 

def feellucky(terms):
	var = requests.get(r'http://www.google.com/search?q="'+terms+r' site:wikipedia.org"&btnI') 
	print var.url
	wikiurl= var.url
	return wiki(wikiurl)


def wiki(wikiurl): # !wiki <search term>
    response = wikiurl
    response = response + '\n' + get_para(response)
    return response

def get_para(wlink):
    'Gets the first paragraph from a wiki link'

    msg = ''
    try:
        page_request = urllib2.Request(wlink)
        page_request.add_header('User-agent', 'Mozilla/5.0')
        page = urllib2.urlopen(page_request)
    except IOError:
        msg = 'Cannot acces link!'
    else:

        soup = BeautifulSoup(page)
        msg = ''.join(soup.find('div', { 'id' : 'bodyContent'}).p.findAll(text=True))

        while 460 < len(msg): # the paragraph cannot be longer than 510
            # characters including the protocol command
            pos = msg.rfind('.')
            msg = msg[:pos]

    return msg
    
def AI(jid,query,querer,group):
	query=query[len("wiki "):]
	result=feellucky(query)
	if group:
		result=querer+": \n"+result
	modules.sender.message_queue(jid,result)

def onMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	if messageContent.lower().startswith("wiki "):
		AI(jid,messageContent,pushName,None)
		
def onGroupMessageReceived(messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
	if messageContent.lower().startswith("wiki "):
		AI(jid,messageContent,pushName,msgauthor)

def setup(super):
	super.signalsInterface.registerListener("message_received", onMessageReceived)
	super.signalsInterface.registerListener("group_messageReceived", onGroupMessageReceived)
	global bot
	bot=super
