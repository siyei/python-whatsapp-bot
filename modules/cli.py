bot=None
from pprint import pprint
from Yowsup.Contacts.contacts import WAContactsSyncRequest
import os

def onCommand(command):
	if command.lower().strip()=="sync":
		contactfile=os.path.join('configs','contacts')
		with open(contactfile,'r') as conts:
			contacts=conts.read()
			contacts = contacts.split(',')
		wsync = WAContactsSyncRequest(bot.username, bot.password, contacts)
		print("Syncing %s contacts" % len(contacts))
		result = wsync.send()
		print(resultToString(result))
	else:
		method,rest=command.split(' ',1)
		print "calling %s with "% method
		rest=tuple(x for x in rest.split())
		pprint(rest)
		bot.methodsInterface.call(method,(rest))
	
def setup(parent):
	parent.signalsInterface.registerListener("command", onCommand)
	global bot
	bot=parent
