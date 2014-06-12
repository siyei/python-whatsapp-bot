from Yowsup.Media.downloader import MediaDownloader 
from Yowsup.Media.uploader import MediaUploader 
from sys import stdout 
import os 
import hashlib 
import base64
import time
import Image
import StringIO


bot=None
outbox=[]
outboxprocessing=False
outboxempty=True
gotMediaReceipt = False
done = False
pathtoimage=""
jid=""
hashimage=""

def onImageReceived(messageId, jid, preview, url, size, wantsReceipt, isBroadcast):
        print("Image received: Id:%s Jid:%s Url:%s size:%s" %(messageId, jid, url, size))
        print preview
        downloader = MediaDownloader(onDlsuccess, onDlerror, onDlprogress)
        downloader.download(url)
        global bot
        if wantsReceipt and bot.sendReceipts:
            bot.methodsInterface.call("message_ack", (jid, messageId))

        timeout = 10
        t = 0;
        while t < timeout:
            time.sleep(0.5)
            t+=1

def onDlsuccess(path):
	print("Image downloded to %s"%path)

def onDlerror():
	stdout.write("\n")
	stdout.flush()
	print("Download Error")

def onDlprogress(progress):
	stdout.write("\r Progress: %s" % progress)
	stdout.flush()



def createThumb(path):
        try:
            size = 100, 100
            im = Image.open(path)
            im.thumbnail(size, Image.ANTIALIAS)
            output = StringIO.StringIO()
            im.save(output,"JPEG")
            contents = output.getvalue()
            output.close()
            #im.save(outfile, "JPEG")
            return base64.b64encode(contents)
        except IOError:
            print "cannot create thumbnail for '%s'" % path
	

def onUploadSuccess(url):
	print("Upload Succ: url: %s "%( url))
	doSendImage(url)

def onError():
	print("Upload Fail:")
	global outboxprocessing
	outboxprocessing=False

def onProgressUpdated(progress):
	stdout.write("\r Progress: %s" % progress)

### send image

def doSendImage(url):
	global pathtoimage,jid
	print("Sending message_image")
	statinfo = os.stat(pathtoimage)
	name=os.path.basename(pathtoimage)
	global bot
	msgId = bot.methodsInterface.call("message_imageSend", (jid, url, name,str(statinfo.st_size), createThumb(pathtoimage)))
	global outboxprocessing
	outboxprocessing=False
	#sentCache[msgId] = [int(time.time()), path]	


## repeated upload

def onmedia_uploadRequestDuplicate(_hash, url):
	print("Request Dublicate: hash: %s url: %s "%(_hash, url))
	doSendImage(url)
	global gotMediaReceipt
	gotMediaReceipt = True

### upload

def uploadImage(url):
	global jid,pathtoimage
	uploader = MediaUploader(jid, bot.username, onUploadSuccess, onError, onProgressUpdated)
	print "going to upload",pathtoimage
	uploader.upload(pathtoimage,url)



### upload request ##


def onmedia_uploadRequestSuccess(_hash, url, resumeFrom):
	print("Request Succ: hash: %s url: %s resume: %s"%(_hash, url, resumeFrom))
	uploadImage(url)
	global gotMediaReceipt
	gotMediaReceipt = True

def onmedia_uploadRequestFailed(_hash):
	print("Request Fail: hash: %s"%(_hash))
	gotReceipt = True
	global outboxprocessing
	outboxprocessing=False


### First step. Get ###

def sendPicture(path):
	if not os.path.isfile(path):
                print("File %s does not exists" % path)
                return 1


	statinfo = os.stat(path)
	name=os.path.basename(path)
	print("Sending picture %s of size %s with name %s" %(path, statinfo.st_size, name))
	mtype = "image"

	sha1 = hashlib.sha256()
	fp = open(path, 'rb')
	try:
		sha1.update(fp.read())
		hsh = base64.b64encode(sha1.digest())
		print("Sending media_requestUpload")
		global bot
		global hashjid,hashpath
		a=bot.methodsInterface.call("media_requestUpload", (hsh, mtype, os.path.getsize(path)))
		print "a is",a
	finally:
		fp.close()

	timeout = 100
	t = 0;
	global gotMediaReceipt
	while t < timeout and not gotMediaReceipt:
		time.sleep(0.5)
		t+=1

	if not gotMediaReceipt:
		print("MediaReceipt print timedout!")
		global outboxprocessing
		outboxprocessing=False
		return 1
	else:
		print("Got request MediaReceipt")
		return
	
		
def photo_process():
	global outboxprocessing
	global outbox
	if ((len(outbox)==0) or outboxprocessing):
		return
	else:
		outboxprocessing=True
		x=outbox.pop(0)
		recepient,path=x
		global pathtoimage, jid
		pathtoimage=path
		jid=recepient
		global bot
		bot.methodsInterface.call("typing_send",(recepient,))
		sendPicture(pathtoimage)
		photo_process()

def photo_queue(recepient,path):
	newmessage=(recepient,path)
	global outbox
	global outboxprocessing
	outbox.append(newmessage)
	photo_process()

def setup(super):
	super.signalsInterface.registerListener("media_uploadRequestSuccess", onmedia_uploadRequestSuccess)
	super.signalsInterface.registerListener("media_uploadRequestFailed", onmedia_uploadRequestFailed)
	super.signalsInterface.registerListener("media_uploadRequestDuplicate", onmedia_uploadRequestDuplicate)
	super.signalsInterface.registerListener("image_received",onImageReceived)
	global path, gotMediaReceipt, done
	global bot
	bot=super
