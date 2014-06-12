import os, errno, json
import modules
from modules.misctools import mkdir_p

bot=None
        
def logger(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	path=os.path.join('logs','incoming',jid)
	if not os.path.exists(path):
		os.makedirs(path)
	filepath=os.path.join(path,messageId)
	with open (filepath,'w') as messagefile:
		json.dump((messageId,jid,messageContent,timestamp,wantsReceipt,pushName,isBroadcast),messagefile)
		global bot
		if wantsReceipt and bot.sendReceipts:
			bot.methodsInterface.call("message_ack",(jid,messageId))
		

def onMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	messageobject=messageId,jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast
	print messageContent
	#messageContent=messageContent.decode('utf8')
	logger(*messageobject)
	modules.sender.message_queue(jid,messageContent)

def onGroupMessageReceived(messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
	messageobject=messageId,jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName
	if wantsReceipt and bot.sendReceipts:
		bot.methodsInterface.call("message_ack", (jid, messageId))
	logger(*messageobject)

def setup(super):
	super.signalsInterface.registerListener("message_received", onMessageReceived)
	super.signalsInterface.registerListener("group_messageReceived", onGroupMessageReceived)
	global bot
	bot=super
