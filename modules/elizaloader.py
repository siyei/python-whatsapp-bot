bot=None

import modules
import modules.eliza as eliza
import os
from BeautifulSoup import BeautifulSoup
from modules.chatterbotapi import ChatterBotFactory, ChatterBotType
factory = ChatterBotFactory()
bot1 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
bot1session = bot1.create_session()

#bot2 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
#bot2session = bot2.create_session()


#if eliza
#therapist = eliza.eliza()

disturbon=[]

def AI(jid,query,querer,group):
	taken=["wiki","google","image"]
	for x in taken:
		if query.lower().startswith(x):
			return
	#global therapist
	#reply = therapist.respond(query)
	global bot1session
	reply = bot1session.think(query)
	VALID_TAGS = ['br']
    	soup = BeautifulSoup(reply)

	for tag in soup.findAll(True):
		if tag.name not in VALID_TAGS:
			tag.hidden = True

	reply=soup.renderContents()
	reply=reply.replace('<br />','\n')
	
	if group:
		if reply!=".":
			modules.sender.message_queue(jid,reply)
	else:
		modules.sender.message_queue(jid,reply)

def onMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	AI(jid,messageContent,pushName,None)

def writedisturb():
	global disturbon
	pathtodisturbances=os.path.join('configs','elizaon')
	with open(pathtodisturbances,'w') as disturbances:
		towrite=""
		for jid in disturbon:
			towrite+=jid+','
		towrite=towrite.rstrip(',')
		disturbances.write(towrite)
		

def onGroupMessageReceived(messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
	global disturbon
	if messageContent.lower().strip()=="shut up":
		print "bot shutting up" 
		leave='FINE! just ask me to "talk" if you are feeling lonely'
		modules.sender.message_queue(jid,leave)
		print disturbon
		disturbon=filter(lambda a: a != jid, disturbon)
		print disturbon
		writedisturb()
	elif jid in disturbon:
		AI(jid,messageContent,pushName,msgauthor)
	elif messageContent.lower().strip()=="talk":
		disturbon.append(jid)
		intro='okay! I will start talking. tell me to "shut up" if i am obnoxious'
		modules.sender.message_queue(jid,intro)
		writedisturb()
	

def setup(parent):
	parent.signalsInterface.registerListener("message_received", onMessageReceived)
	parent.signalsInterface.registerListener("group_messageReceived", onGroupMessageReceived)
	global disturbon
	pathtodisturbances=os.path.join('configs','elizaon')
	try:
		with open(pathtodisturbances,'r') as disturbances:
			disturbances=disturbances.read()
			disturbon=disturbances.split(',')
	except IOError:
		pass
		
	global bot
	bot=parent
