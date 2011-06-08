#!/usr/bin/python############################################################################## wagtail - Open Source Medical Messaging# ---------------------------------------------------------------------------############################################################################## This source code is protected by the GPL v2 or later licensing scheme.# Details regarding the GPL v2 or later are available at http://www.gnu.org# You may use and share it as long as you don't deny this right# to anybody else.## wagMail# This file contains email functions in relation to wagtail.#############################################################################try:    import GnuPGInterfaceexcept ImportError:    print "You need to have GnuPGInterface installed. It is available from http://py-gnupg.sourceforge.net/"class gmKeysClass(GnuPGInterface.GnuPG):	"Class to provide interface between GnuPG and Python"	def __init__(self):		GnuPGInterface.GnuPG.__init__(self)		self.setup_my_options()	def setup_my_options(self):		self.options.armor = 1		self.options.meta_interactive = 0		self.options.extra_args.append('--no-secmem-warning')			def decryptString(self,password,toAddr,ciphertext):		"Decrypts GPG ciphertext and status=1, but returns original and status=0 if error"		try:			self.passphrase = password			self.options.recipients = [toAddr]					p1 = self.run(['--decrypt'], create_fhs=['stdin', 'stdout','logger'])			p1.handles['stdin'].write(ciphertext)			p1.handles['stdin'].close()			plaintext = p1.handles['stdout'].read()			p1.handles['stdout'].close()			loggertext = p1.handles['logger'].read()			p1.handles['logger'].close()					# process cleanup			p1.wait()			#print "loggertext is %s" %(loggertext)			print "Message successfully decrypted"			status=1		except:			print "Error : Unable to decrypt"			print sys.exc_type," : ",sys.exc_value			status=0			plaintext=ciphertext		return (plaintext,status)		def pollMails(POP3server, POP3user, POP3password, destFolder):	"Retrieve mail from server, place in In Folder, delete from server, send ack, log"	import poplib,re,sys,time	print "Checking mail from %s" %(POP3server)	try:		M = poplib.POP3(POP3server)		M.user(POP3user)		M.pass_(POP3password)		numMessages = len(M.list()[1])		print "Downloading %i messages" %(numMessages)		for i in range(numMessages):			lines = M.retr(i+1)[1] 			rawmsg = '\n'.join(lines)			# get relevant headers			fromText=re.search(r'From:(?P<From>.+)\n',rawmsg).group('From')			dateText=re.search(r'Date:(?P<Date>.+)\n',rawmsg).group('Date')			idText=re.search(r'Message-Id:\s+<(?P<MessageID>.+)@',rawmsg).group('MessageID')			subjectText=re.search(r'Subject:(?P<Subject>.+)\n',rawmsg).group('Subject')			print "Receiving %s" %(subjectText)			# save rawmsg into tmp folder			try:				fileName=destFolder+'/In/'+idText				file=open(fileName,"w")				file.write(rawmsg)				file.close()				# message successfully saved, so remove from server				# hash out for testing purposes				M.dele(i+1)				#this is where one would send acknowledgment of receipt				ackSend(idText,fromText)				# add to logFile				# logFile contains time that file was downloaded, not sent				theTime=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())								logText="RCPT "+theTime+" "+idText+"  "+subjectText+ " ("+fromText+")\n"				wagLog('mail',logText)			except:				print "Error in saving to In box\n"				print sys.exc_type, ":", sys.exc_value		M.quit()	except poplib.error_proto, detail:   		print "POP3 Protocol Error:", detaildef ackSend(MsgID,address):	passdef processInbox(mailFolder):	"for each file in Mail/In, process, move to mail/Read"	import os,email,re	from email import Parser	for root, dirs, files in os.walk(mailFolder+"/In"):		for name in files:			print "first letter is %s" %(name[1])			print "Processing %s" %(name)			file=open(mailFolder+"/In/"+name,"r")			msg=email.message_from_file(file)			file.close()			msg=decryptMsgPGP(msg,name)			msg=decryptMsgCA(msg,name)				# Move to Read folder. Hash out for testing			os.rename(mailFolder+"/In/"+name,mailFolder+"/Read/"+name)			# Write decrypted file to Decrypted folder			msgStr=msg.as_string()			fromAddr=re.search(r'From:(?P<From>.+)\n',msgStr).group('From')			file=open(mailFolder+"/Decrypted/"+name,"w")			file.write(msgStr)			file.close()			#add to mbox for user			file=open(mailFolder+"/usr/"+username,"a")			file.write("From "+fromAddr+"\n"+msgStr+"\n")			file.close()						def decryptMsgPGP(msg,name):	import string	gnupg = gmKeysClass()	"divide each message into its MIME parts and deal with as each requires"	PGPFlag=0		for part in msg.walk():				decoded=part.get_payload(decode=1)				# Determine the MIME type and deal with appropriately		# Check for inline PGP		if  part.get_content_type() =='text/plain' and string.find(decoded,'BEGIN PGP MESSAGE')>0:			passphrase=getPassphrase()			plaintext,status=gnupg.decryptString(passphrase,accountAddress,decoded)			if status==0:				plaintext=decoded			else:				part.set_payload(plaintext)				PGPFlag=1				#signedFlag=gnupg.verifyString(plaintext)								# Check for PGP encoded MIME		if  part.get_content_type() =='application/octet-stream' and string.find(decoded,'BEGIN PGP MESSAGE')>0:			passphrase=getPassphrase()			plaintext,status=gnupg.decryptString(passphrase,accountAddress,decoded)			print "status is %s" %(status)			if status==0:				plaintext=decoded			else:					part.set_payload(plaintext)			PGPFlag=1	if PGPFlag:		logText="PGP decrypt "+name		wagLog('mail',logText)			return msgdef decryptMsgCA(msg,name):	return msgdef getPassphrase():	import getpass	# will put in a time checking procedure here so that passphrase is remembered for	# user-defined period.	passphrase=getpass.getpass("Your passphrase: ")	return passphrase		def wagLog(logName,logText):	"add to log - mail,....."	try:		file=open(logFolder+"/"+logName+".log","a")		file.write(logText)		file.close()	except:		print "Error in writing to mail.log file\n"		print sys.exc_type, ":", sys.exc_value						if __name__ == "__main__":	#------------------------------------------	#Config options 	# these will need to be moved to a separate config file	logFolder="logs"	POP3server='medicineau.net.au'	POP3user='wagtail'	POP3password='password'	mailFolder='mail'	# mail folder requires subdirectories In, Read, Decrypted	# to do - create these subdirectories automatically	keyServer='keyserver.medicine.net.au'	# account address is the address for the private GPG key	# would normally be POP3user@POP3server	accountAddress='tony@lemlink.com.au'	username='tony'	# usu config would be smtpServer='localhost'	#I use medicineau.net.au	smtpServer='medicineau.net.au'	#smtpServer='localhost'	# -----------------------------------------	#	import string	import M2Crypto	pollMails(POP3server,POP3user,POP3password,mailFolder)	processInbox(mailFolder)						