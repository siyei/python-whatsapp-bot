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

path = os.path.abspath(os.path.dirname(__file__))
if not path in sys.path:
    sys.path.append(path)
yowsuppath=os.path.join(path,'./yowsup/src/')
if not yowsuppath in sys.path:
    sys.path.append(os.path.join(path,'./yowsup/src/'))

DEFAULT_CONFIG = os.path.join(path,'configs/config')

del path


from Yowsup.Common.utilities import Utilities

def main():

	parser = argparse.ArgumentParser(description='Python Whatsapp Bot Command line options')
	parser.add_argument('-b','--bot', help='Bot', action="store_true", required=False, default=False)
	parser.add_argument('-a','--autoack', help='If used with -l or -i, then a message received ack would be automatically sent for received messages', action="store_true", required=False, default=False)
	parser.add_argument('-k','--keepalive', help="The bot will automatically respond to server's ping requests to keep connection alive", action="store_true", required=False, default=False)
	parser.add_argument('-c','--config', help="Path to config file containing authentication info. For more info about config format use --help-config", action="store", metavar="file", required=False, default=False)
	args = vars(parser.parse_args())

	def getCredentials(self,config = DEFAULT_CONFIG):
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

	if len(sys.argv) == 1:
		parser.print_help()
	else:
		credentials = getCredentials(args["config"] or DEFAULT_CONFIG)
		if credentials:
			countryCode, login, identity, password = credentials
			password = base64.b64decode(bytes(password.encode('utf-8')))
			if args["bot"]:
				bot = Bot(login,password,args['keepalive'], args['autoack'])
				bot.run()

class Bot:
	def __init__(self,login,password,keepalive=False,autoack=False):
		print "bot created"
		
	def run(self):
		print "run"
	
	
if __name__=="__main__":
	main()
