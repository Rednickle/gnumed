#======================================================================
# GnuMed patient EMR browser plugin
# ----------------------------------------------
#
# this plugin holds patient EMR tree
#
# @copyright: author
#======================================================================
__version__ = "$Revision: 1.3 $"
__author__ = "Carlos Moro"
__license__ = 'GPL (details at http://www.gnu.org)'

from Gnumed.wxpython import gmPlugin, gmEMRBrowser
from Gnumed.pycommon import gmLog

_log = gmLog.gmDefLog
_log.Log(gmLog.lInfo, __version__)

#======================================================================
class gmEMRBrowserPlugin(gmPlugin.cNotebookPlugin):
	"""Plugin to encapsulate patient EMR browser window."""

	tab_name = _('EMR browser')

	def name (self):
		return gmEMRBrowserPlugin.tab_name

	def GetWidget (self, parent):
		self._widget = gmEMRBrowser.cEMRBrowserPanel(parent, -1)
		return self._widget

	def MenuInfo (self):
		return ('tools', 'EMR &browser')

	def can_receive_focus(self):
		# need patient
		if not self._verify_patient_avail():
			return None
		return 1
		    
#======================================================================
# main
#----------------------------------------------------------------------
if __name__ == "__main__":

    import sys
    from wxPython import wx

    from Gnumed.pycommon import gmPG, gmCfg
    from Gnumed.exporters import gmPatientExporter

    _cfg = gmCfg.gmDefCfgFile	
	
    _log.Log (gmLog.lInfo, "starting emr browser plugin...")

    if _cfg is None:
        _log.Log(gmLog.lErr, "Cannot run without config file.")
        sys.exit("Cannot run without config file.")

    try:
        # make sure we have a db connection
        gmPG.set_default_client_encoding('latin1')
        pool = gmPG.ConnectionPool()
        
        # obtain patient
        patient = gmEMRBrowser.askForPatient()
        if patient is None:
            print "None patient. Exiting gracefully..."
            sys.exit(0)
                    
        # display standalone browser
        application = wx.wxPyWidgetTester(size=(800,600))
        emr_browser = gmEMRBrowser.cEMRBrowserPanel(application.frame, -1)
        emr_browser.refresh_tree()
        
        application.frame.Show(True)
        application.MainLoop()
        
        # clean up
        if patient is not None:
            try:
                patient.cleanup()
            except:
                print "error cleaning up patient"
    except StandardError:
        _log.LogException("unhandled exception caught !", sys.exc_info(), 1)
        # but re-raise them
        raise
    try:
        pool.StopListeners()
    except:
        _log.LogException('unhandled exception caught', sys.exc_info(), verbose=1)
        raise

    _log.Log (gmLog.lInfo, "closing emr browser plugin...")

#======================================================================
# $Log: gmEMRBrowserPlugin.py,v $
# Revision 1.3  2004-10-31 00:35:40  cfmoro
# Fixed some method names. Added sys import. Refesh browser at startup in standalone mode
#
# Revision 1.2  2004/09/25 13:12:15  ncq
# - switch to from wxPython import wx
#
# Revision 1.1  2004/09/06 18:59:18  ncq
# - Carlos wrote a plugin wrapper for us
#
