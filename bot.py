#!/usr/bin/python

'''
Copyright (c) <2014> Akshay S Dinesh <asdofindia@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

__author__ = "Akshay S Dinesh"
__version__ = "0.1"
__email__ = "asdofindia@gmail.com"
__license__ = "MIT"

import argparse, sys, os, csv
import threading,time, base64
import logging 

path = os.path.abspath(os.path.dirname(__file__))
if not path in sys.path:
    sys.path.append(path)
yowsuppath=os.path.join(path,'./yowsup/src/')

if not yowsuppath in sys.path:
    sys.path.append(os.path.join(path,'./yowsup/src/'))
    
DEFAULT_CONFIG = os.path.join(path,'configs/config')

del path


from Yowsup.Common.utilities import Utilities
from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.debugger import Debugger
from Yowsup.Common.constants import Constants

import modules


def getCredentials(config = DEFAULT_CONFIG):
	if os.path.isfile(config):
		f = open(config)
		phone = ""
		idx = ""
		pw = ""
		cc = ""
		try:
			for l in f:
				line = l.strip()
				if len(line) and line[0] not in ('#',';'):
					prep = line.split('#', 1)[0].split(';', 1)[0].split('=', 1)
					varname = prep[0].strip()
					val = prep[1].strip()
					if varname == "phone":
						phone = val
					elif varname == "id":
						idx = val
					elif varname =="password":
						pw =val
					elif varname == "cc":
						cc = val
			return (cc, phone, idx, pw);
		except:
			pass
	return 0

def main():
	logging.info("main running")
	parser = argparse.ArgumentParser(description='Python Whatsapp Bot Command line options')
	parser.add_argument('-b','--bot', help='Bot', action="store_true", required=False, default=False)
	parser.add_argument('-a','--autoack', help='If used with -l or -i, then a message received ack would be automatically sent for received messages', action="store_true", required=False, default=False)
	parser.add_argument('-k','--keepalive', help="The bot will automatically respond to server's ping requests to keep connection alive", action="store_true", required=False, default=False)
	parser.add_argument('-c','--config', help="Path to config file containing authentication info. For more info about config format use --help-config", action="store", metavar="file", required=False, default=False)
	parser.add_argument('-l','--log', help="The log level", action="store", required=False,metavar="loglevel")
	args = vars(parser.parse_args())

	if len(sys.argv) == 1:
		parser.print_help()
	else:
		Debugger.enabled=False #disabling yowsup debugger This will also create problems with logging. So can't use them for now
		if args["log"]:
			loglevel=args["log"]
			#logging.shutdown()
			#reload(logging)
			#numeric_level = getattr(logging, loglevel.upper(), None)
			#if not isinstance(numeric_level, int):
	    		#	raise ValueError('Invalid log level: %s' % loglevel)
			#logging.basicConfig(level=numeric_level)
			#logging.basicConfig(level=logging.DEBUG,filename="configs/log", format='%(levelname)s:%(message)s')
			#logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
		credentials = getCredentials(args["config"] or DEFAULT_CONFIG)
		logging.info("have been used to load")
		logging.info(credentials)
		if credentials:
			logging.info("credentials loaded")
			countryCode, login, identity, password = credentials
			password = base64.b64decode(bytes(password.encode('utf-8')))
			if args["bot"]:
				bot = Bot(login,password,args['keepalive'], args['autoack'])
				bot.run()
		else:
			logging.error("couldn't load credentials")

class Bot:
	def __init__(self,login,password,keepAlive=False,autoack=False):
		logging.info("bot created")
		self.sendReceipts = autoack
		self.username=login
		self.password=password
		self.stayon=True
		#self.setup()
		connectionManager = YowsupConnectionManager()
		connectionManager.setAutoPong(keepAlive)
		
		dirs=["downloads","logs","modules","configs"]
		for folder in dirs:
			if not os.path.isdir(folder):
				print "missing directory %s. Creating it." % folder
				modules.misctools.mkdir_p(folder)
		
		self.signalsInterface = connectionManager.getSignalsInterface()
		self.methodsInterface = connectionManager.getMethodsInterface()
		
		self.signalsInterface.signals.append("command")
		
		self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
		self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
		self.signalsInterface.registerListener("disconnected", self.onDisconnected)
		
		for module in vars(modules).values():
			if hasattr(module,"setup"):
				module.setup(self)
		
		
	def run(self):
		logging.info("bot started running")
		self.login()
	
	def login(self):
		username=self.username
		password=self.password
		self.methodsInterface.call("auth_login", (username, password))
		self.methodsInterface.call("presence_sendAvailable",)
		print "online\n"
		while self.stayon:
			command=raw_input()
			if command=="/quit":
				self.stayon=False
			else:
				self.onCommand(command)
				continue

	def onAuthSuccess(self, username):
		print "Authed %s" % username
		self.methodsInterface.call("ready")

	def onAuthFailed(self, username, err):
		print "Auth Failed!"

	def onDisconnected(self, reason):
		print "Disconnected because %s" %reason
		if reason=="dns": time.sleep(30)
		time.sleep(1)
		self.login()


				
	def onCommand(self,command):
		self.signalsInterface.send("command",(command,))
		pass
		
	
if __name__=="__main__":
	main()
