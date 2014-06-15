import json
import modules

bot=None

def onclientinfochange():
	global bot
	clientsinfo=bot.clientsinfo
	with open(bot.clientsinfofile,'w') as clientinfofileobj:
		json.dump(clientsinfo,clientinfofileobj)
		

def AI(jid,message,querer,group):
	global bot
	try:
		clientinfo=bot.clientsinfo[jid]
	except KeyError:
		if bot.admin in jid:
			clientinfo={'okaytotalk':True}
			bot.clientsinfo[jid]=clientinfo
		else:
			clientinfo={'okaytotalk':False,'sentprereqs':False}
			bot.clientsinfo[jid]=clientinfo
	if not clientinfo['okaytotalk']:
		if not clientinfo['sentprereqs']:
			preprereqs="Hi there! Before you start (ab)using me, I need to make sure the suffering is worth it. Please copy paste the registration form below and fill out the details INSIDE the square brackets : [like this]. Do not edit anything outside. Do not remove the square brackets. Send it back right here."
			if group:
				preprereqs+="\nIf you choose not to register within 50 messages I will leave the group automatically"
				prereqs="Auth code=%s\nRegistration form for group use. \nGroup name: []\nGroup admin name: []\nGroup admin email: []\nGroup admin phone: []\nGroup admin occupation: []\nBrief description of group activity: []\nHow did you come to know about me?: []\nEnd of registration form" % jid
			else:
				prereqs="Auth code=%s\nRegistration form for individual use. \nYour name: []\nEmail address: []\nPhone number: []\nOccupation: []\nHow did you come to know about me?: []\nEnd of registration form" % jid
			postreqs="By registering, you agree to the following terms and conditions.\n0. My owner has the right to stop running me AT ANY TIME\n1. You agree to not use me in any way that will cause trouble to my owner, the humanity, or the universe.\n\nAdditional info:\nI am open source and released under the MIT license. Visit github.com/asdofindia/python-whatsapp-bot to view/clone/contribute to my source code.\nCredits:\n* pandorabots.com for their demo bots\n* Tarek Galal for Yowsup library\n* Akshay S Dinesh for fathering me"
			modules.sender.message_queue(jid,preprereqs)
			modules.sender.message_queue(jid,prereqs)
			modules.sender.message_queue(jid,postreqs)
			clientinfo['sentprereqs']=True
			bot.clientsinfo[jid]=clientinfo
			onclientinfochange()
		else:
			try:
				clientinfo['messagecount']+=1
			except KeyError:
				clientinfo['messagecount']=1
			if clientinfo['messagecount']>50:
				if group:
					bot.methodsInterface.call("group_end",(jid,))
			registrationdetails=message.split('\n')
			if registrationdetails[0]==("Auth code="+jid):
				registrationtried=True
				regdetails={}
				try:
					registrationdetails=registrationdetails[2:-1]
					errormessage=""
					for detail in registrationdetails:
						detailsplit=detail.split(': ')
						question=detailsplit[0]
						answer=detailsplit[1].strip('[]').strip()
						if not answer:
							errormessage+="Please fill the field: %s\n" % question
						else:
							regdetails[question]=answer
					if errormessage:
						errormessage+="Resubmit the registration form with correct details. Do not edit anything outside the square brackets."
						registrationfailed=True
					else:
						registrationfailed=False
				except IndexError:
					errormessage="Please copy paste the registration form and fill it carefully with correct details. Do not edit anything outside the square brackets"
					registrationfailed=True
				if registrationfailed:
					modules.sender.message_queue(jid,errormessage)
				else:
					successmessage="Registration succeeded. Please bear in mind that my owner will be checking the registration details and ban  you if they are bogus details"
					modules.sender.message_queue(jid,successmessage)
					clientinfo['okaytotalk']=True
					clientinfo['regdetails']=regdetails
					bot.clientsinfo[jid]=clientinfo
					onclientinfochange()
					
				

def onMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	AI(jid,messageContent,pushName,None)
		
def onGroupMessageReceived(messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
	AI(jid,messageContent,pushName,msgauthor)

def setup(parent):
	parent.signalsInterface.registerListener("message_received", onMessageReceived)
	parent.signalsInterface.registerListener("group_messageReceived", onGroupMessageReceived)
	global bot
	bot=parent
