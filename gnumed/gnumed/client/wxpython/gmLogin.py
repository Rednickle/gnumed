#!/usr/bin/python
#############################################################################
#
# gmLogin - Display a login dialog and log onto backend(s)
# ---------------------------------------------------------------------------
#
# @author: Dr. Horst Herb
# @copyright: author
# @license: GPL (details at http://www.gnu.org)
# @dependencies: gmPG, gmLoginInfo
# @change log:
#	29.10.2001 hherb first draft, untested
#
# @TODO: testing
############################################################################

from wxPython.wx import *
import os.path
import gmLoginDialog, gmPG, gmGuiBroker, gmLog, gmExceptions

def Login(max_attempts=3):
	"""Display the login dialog and try to log into the backend up to max_attempts times
	Returns either a valid backend broker object if connection was succesful, or None."""

	logged_in = false
	attempts = 0
	backend = None
	#display the login dialog
	broker = gmGuiBroker.GuiBroker ()
	# CHANGED CODE Haywood 26/2/02
	#: use global variable to find image file  
	dlg = gmLoginDialog.LoginDialog(None, -1)
	dlg.Centre(wxBOTH)
	while not logged_in and attempts < max_attempts:
		dlg.ShowModal()
		#get the login parameters
		login = dlg.panel.GetLoginInfo()
		if login is None:
			#user cancelled
			dlg.Destroy()
			myLog.Log(gmLog.lInfo, _("user cancelled login dialog"))
			return None
		# FIXME: this is security sensitive because of passwords
		myLog.Log(gmLog.lData, _("login parameters: ") + str(login))
		myLog.Log(gmLog.lInfo, _("login attempt #") + str(attempts) + _(" of ") + str(max_attempts))
		#now try to connect to the backend
		try:
			backend = gmPG.ConnectionPool(login)
			logged_in = true
			myLog.Log(gmLog.lInfo, _("backend connection successfully established"))
		except gmExceptions.ConnectionError, e:
			attempts+=1
			myLog.Log(gmLog.lWarn, _("backend connection failed"))
			if attempts < max_attempts:
				wxMessageBox(_("Login failed because: %s\nPlease retry or cancel" % e))
	dlg.Close()
	dlg.Destroy()
	return backend

#--------------------------------------------------------------
myLog = gmLog.gmDefLog

if __name__ == "__main__":
	import gmI18N
	myLog.Log (gmLog.lWarn, "This module needs a test function!  please write it")
	print "This module needs a test function!  please write it"
