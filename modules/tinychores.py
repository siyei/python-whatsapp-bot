bot=None

#call 	message_ack(str jid,int messageId)
#	notification_ack(str jid,int messageId)
#	delivered_ack(str jid,int messageId)
#	visible_ack(str jid,int messageId)
#	subject_ack(str jid,int messageId)

def onProfileSetStatusSuccess(jid,messageId):
	print "profile status changed successfully! %s %s" % (jid,messageId)
	global bot
	bot.methodsInterface.call("notification_ack",(jid,messageId))

def onMessageDelivered(jid,messageId):
	#print "message delivered %s %s" % (jid,messageId)
	print "delivered"
	global bot
	#bot.methodsInterface.call("delievered_ack",(jid,messageId))
	bot.methodsInterface.call("message_ack",(jid,messageId))

def onMessageSent(jid,messageId):
	#print "sent %s %s" % (jid,messageId)
	print "sent"
	global bot
	#bot.methodsInterface.call("delievered_ack",(jid,messageId))
	bot.methodsInterface.call("message_ack",(jid,messageId))
	

	
def onVisible(jid,messageId):
	print "visible: %s %s" % (jid,messageId)

def onStatusDirty():
	print "status dirty. if I knew what that means"



def onMessageError(messageId,jid,errorCode):
	print "message error %s %s %s" % (messageId,jid,errorCode)

def onGroup_gotinfo(jid, owner, subject, subjectOwner, subjectTimestamp, creationTimestamp):
	print "group %s is owned by %s has the subject %s set by %s" % (jid,owner,subject,subjectOwner)
	
def onGroup_setsubjectsuccess(jid):
	print "group %s subject set " %jid

def onGroup_subjectreceived(messageId, jid, author, subject, timestamp, receiptRequested):
	global bot
	bot.methodsInterface.call("notification_ack",(jid,messageId))
	print "group %s subject changed to %s by %s" % (jid,subject, author)
		
def onGroup_addparticipantssuccess(jid,gjid):
	print "adding participant success"
	print jid,gjid
	
def onGroup_removeparticipantssuccess(jid):
	print "participant removed"
	
def onGroup_createsuccess(groupJid):
	print "group %s created" %groupJid	
	
def onGroup_createfail(errorCode):
	print "group creationg failed"
	
def onGroup_endsuccess(jid):
	print "left group %s" % jid
	
def onGroup_gotpicture(jid, filePath):
	print "group %s pic changed to %s" % (jid,filePath)
	
def onGroup_infoerror(errorCode):
	print "group infoerror %s" % errorCode
	
def onGroup_gotparticipants(jid, jids):
	print "group %s participants are" % jid,
	for x in jids:
		print x,
		
def onGroup_setpicturesuccess(jid):
	print "group %s picture set" % jid
	
def onGroup_setpictureerror(jid, errorCode):
	print "couldn't set group picture"

	
def setup(parent):
	parent.signalsInterface.registerListener("profile_setStatusSuccess", onProfileSetStatusSuccess)
	parent.signalsInterface.registerListener("receipt_messageSent", onMessageSent)
	parent.signalsInterface.registerListener("receipt_visible", onVisible) 
	parent.signalsInterface.registerListener("receipt_messageDelivered", onMessageDelivered)
	parent.signalsInterface.registerListener("status_dirty", onStatusDirty)
	parent.signalsInterface.registerListener("message_error", onMessageError)
	
	parent.signalsInterface.registerListener("group_gotInfo", onGroup_gotinfo)
	parent.signalsInterface.registerListener("group_setSubjectSuccess", onGroup_setsubjectsuccess)
	parent.signalsInterface.registerListener("group_subjectReceived", onGroup_subjectreceived)
	parent.signalsInterface.registerListener("group_addParticipantsSuccess", onGroup_addparticipantssuccess)
	parent.signalsInterface.registerListener("group_removeParticipantsSuccess", onGroup_removeparticipantssuccess)
	parent.signalsInterface.registerListener("group_createSuccess", onGroup_createsuccess)
	parent.signalsInterface.registerListener("group_createFail", onGroup_createfail)
	parent.signalsInterface.registerListener("group_endSuccess", onGroup_endsuccess)
	parent.signalsInterface.registerListener("group_gotPicture", onGroup_gotpicture)
	parent.signalsInterface.registerListener("group_infoError", onGroup_infoerror)
	parent.signalsInterface.registerListener("group_gotParticipants", onGroup_gotparticipants)
	parent.signalsInterface.registerListener("group_setPictureSuccess", onGroup_setpicturesuccess)
	parent.signalsInterface.registerListener("group_setPictureError", onGroup_setpictureerror)
	
	global bot
	bot=parent
