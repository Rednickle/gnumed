"""GnuMed GUI helper classes and functions

This module provides some convenient wxPython GUI
helper thingies that are widely used throughout
GnuMed.

This source code is protected by the GPL licensing scheme.
Details regarding the GPL are available at http://www.gnu.org
You may use and share it as long as you don't deny this right
to anybody else.
"""
# ========================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmGuiHelpers.py,v $
# $Id: gmGuiHelpers.py,v 1.1 2003-08-21 00:11:48 ncq Exp $
__version__ = "$Revision: 1.1 $"
__author__  = "K. Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL (details at http://www.gnu.org)"

import sys

if __name__ == '__main__':
	print "This is not intended to be run standalone !"
	sys.exit(-1)

from wxPython.wx import *

import gmLog
_log = gmLog.gmDefLog
_log.Log(gmLog.lData, __version__)
# ========================================================================
def gm_show_error(self, aMessage = None, aTitle = None, aLogLevel = None):
	if aMessage is None:
		aMessage = _('programmer forgot to specify error message')

	if aLogLevel is not None:
		log_msg = str.replace(aMessage, '\015', ' ')
		log_msg = str.replace(log_msg, '\012', ' ')
		_log.Log(aLogLevel, log_msg)

	aMessage = aMessage + _("\n\nPlease consult the error log for all the gory details !")

	if aTitle is None:
		aTitle = _('generic error message dialog')

	dlg = wxMessageDialog(
		NULL,
		aMessage,
		aTitle,
		wxOK | wxICON_ERROR
	)
	dlg.ShowModal()
	dlg.Destroy()
	return 1
#-------------------------------------------------------------------------
def gm_show_question(self, aMessage = None, aTitle = None):
	# sanity checks
	if aMessage is None:
		aMessage = _('programmer forgot to specify question')
	if aTitle is None:
		aTitle = _('generic user question dialog')

	dlg = wxMessageDialog(
		NULL,
		tmp,
		aTitle,
		wxYES_NO | wxICON_QUESTION
	)
	btn_pressed = dlg.ShowModal()
	dlg.Destroy()
	return btn_pressed
# ========================================================================
# $Log: gmGuiHelpers.py,v $
# Revision 1.1  2003-08-21 00:11:48  ncq
# - adds some widely used wxPython GUI helper functions
#
