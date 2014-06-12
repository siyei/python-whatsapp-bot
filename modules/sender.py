import os,json
from modules.misctools import mkdir_p
import time

bot=None
outbox=[]
outboxprocessing=False
outboxempty=True

def message_send(recepient, content):
	#jid=findjidbynick(recepient)
	jid=recepient
	content=content.encode('utf-8')
	messageId = bot.methodsInterface.call("message_send",(jid,content))
	print "sent %s to %s" % (content,jid)
	path=os.path.join('logs','outgoing',jid)
	if not os.path.exists(path):
		os.makedirs(path)
	filepath=os.path.join(path,messageId)
	with open (filepath,'w') as messagefile:
		json.dump((messageId,jid,content,int(time.time())),messagefile)		

def onMessageSent(*args):
	#print "message sent",args
	pass

def onMessageDelivered(*args):
	pass
	#print "message delivered",args

def message_queue(recepient, content):
	newmessage=(recepient,content)
	global outbox
	global outboxempty
	global outboxprocessing	
	outbox.append(newmessage)
	outboxempty=False
	if (outboxempty or outboxprocessing):
		return
	else:
		outboxprocessing=True
		while ((len(outbox))!=0):
				x=outbox.pop(0)
				recepient,content=x
				global bot
				bot.methodsInterface.call("typing_send",(recepient,))
				time.sleep(0.1)
				message_send(recepient,content)
		outboxprocessing=False
		return
		
def setup(parent):
	parent.signalsInterface.registerListener("receipt_messageSent", onMessageSent)
	parent.signalsInterface.registerListener("receipt_messageDelivered", onMessageDelivered)
	global bot
	bot=parent
