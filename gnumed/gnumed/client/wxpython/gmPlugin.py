"""gmPlugin - base classes for GnuMed notebook plugins.

@copyright: author
@license: GPL (details at http://www.gnu.org)
"""
############################################################################
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmPlugin.py,v $
# $Id: gmPlugin.py,v 1.25 2004-07-15 07:57:20 ihaywood Exp $
__version__ = "$Revision: 1.25 $"
__author__ = "H.Herb, I.Haywood, K.Hilbert"

import os, sys, re

from wxPython.wx import *

from Gnumed.pycommon import gmExceptions, gmGuiBroker, gmPG, gmLog, gmCfg, gmWhoAmI, gmDispatcher, gmSignals
from Gnumed.wxpython import gmShadow
from Gnumed.pycommon.gmPyCompat import *

gmPatient = None

_log = gmLog.gmDefLog
_log.Log(gmLog.lInfo, __version__)
_whoami = gmWhoAmI.cWhoAmI()

#==================================================================
class wxNotebookPlugin:
	"""Base class for plugins which provide a full notebook page.
	"""
	def __init__(self, set=None):
		self.gb = gmGuiBroker.GuiBroker()
		self.db = gmPG.ConnectionPool()
		self._set = 'gui'
		# make sure there's a raised_plugin entry
		try:
			tmp = self.gb['main.notebook.raised_plugin']
		except KeyError:
			self.gb['main.notebook.raised_plugin'] = 'none'
		self._widget = None
		self.raised = 0
	#-----------------------------------------------------
	def register (self):
		"""Register ourselves with the main notebook widget."""

		self.gb['modules.%s' % self._set][self.__class__.__name__] = self
		_log.Log(gmLog.lInfo, "plugin: [%s] (class: [%s]) set: [%s]" % (self.name(), self.__class__.__name__, self._set))

		if self.__class__.label is None:
			label = self.name ()
		else:
			label = self.__class__.label
		if self.__class__.widget is None:
			widget = self.GetWidget
		else:
			widget = self.__class__.widget
		gmDispatcher.connect (self.on_display, gmSignals.display_plugin ())
		gmDispatcher.send (gmSignals.new_notebook (), sender=self, widget=widget,
				   label=label, icon=self.__class__.icon,
				   help=self.__class__.help_string,
				   name=self.__class__.__name__)
		return 1

	def on_load (self, *args):
		self.register ()
	#-----------------------------------------------------
	def unregister(self):
		"""Remove ourselves."""
		
		_log.Log(gmLog.lInfo, "plugin: [%s] (class: [%s]) set: [%s]" % (self.name(), self.__class__.__name__, self._set))

		gmDispatcher.send (gmSignals.unload_plugin (), sender=self, name=self.__class__.__name__)
	#-----------------------------------------------------
	icon = None
	help_string = ""
	widget = None # hack for old-style plugins
	label = None
	#-----------------------------------------------------
	def populate_with_data(self):
		print "missing", self.__class__.__name__, "-> populate_with_data()"
	#-----------------------------------------------------
	def on_display (self, name):
		"""We *are* receiving focus now."""
		if name == self.__class__.__name__:
			# yep, that's us
			if self.can_receive_focus ():
				self.raised = 1
				try:
					self.populate_with_data()
				except:
					_log.LogException("problem with populate-with-data ()", sys.exc_info(), verbose=0)
			else:
				return 'veto'
		elif self.raised:
			# somebody else now
			self.raised = 0
			# FIXME: we might want to do something here
	#-----------------------------------------------------
	def can_receive_focus(self):
		"""Called when this plugin is *about to* receive focus.

		If None returned from here (or from overriders) the
		plugin activation will be veto()ed (if it can be).
		"""
		# FIXME: fail if locked
		return 1
	#-----------------------------------------------------
	def _verify_patient_avail(self):
		"""Check for patient availability.

		- convenience method for your can_receive_focus() handlers
		"""
		global gmPatient
		if gmPatient is None:
			from Gnumed.business import gmPatient as _gmPatient
			gmPatient = _gmPatient
		# fail if no patient selected
		pat = gmPatient.gmCurrentPatient()
		if not pat.is_connected():
			# FIXME: people want an optional red backgound here
			self._set_status_txt(_('Cannot switch to [%s]: no patient selected') % self.name())
			wxBell()
			return None
		return 1
	#-----------------------------------------------------
	def _set_status_txt(self, txt):
		set_statustext = self.gb['main.statustext']
		set_statustext(txt)
		return 1
	#-----------------------------------------------------
	def Raise(self):
		"""Raise ourselves."""
		# already raised ?
		if self.gb['main.notebook.raised_plugin'] == self.__class__.__name__:
			return 1
		plugin_list = self.gb['main.notebook.plugins']
		plugin_idx = plugin_list.index(self)
		nb = self.gb['main.notebook']
		nb.SetSelection(plugin_idx)
		return 1
	#-----------------------------------------------------
	#----------------------------------------------------
	def populate_toolbar (self, tb, widget):
		"""Populates the toolbar for this widget.

		- tb is the toolbar to populate
		- widget is the widget returned by GetWidget()		# FIXME: is this really needed ?
		"""
		pass
	# -----------------------------------------------------
	# event handlers for the popup window
	def on_load (self, evt):
		# FIXME: talk to the configurator so we're loaded next time
		self.register()
		# FIXME: raise ?
	# -----------------------------------------------------
	def OnShow (self, evt):
		self.register() # register without changing configuration
	#--------------------------------------------------------
	def GetWidget (self, parent):
		return None
#=========================================================
# some convenience functions
#---------------------------------------------------------
def raise_notebook_plugin(plugin_name = None):
	"""plugin_name is a plugin internal name"""
	gb = gmGuiBroker.GuiBroker()
	try:
		plugin = gb['modules.gui'][plugin_name]
	except KeyError:
		_log.LogException("cannot raise [%s], plugin not available" % plugin_name, sys.exc_info(), verbose=0)
		return None
	if plugin.can_receive_focus():
		plugin.Raise()
		return 1
	return 0
#------------------------------------------------------------------
def instantiate_plugin(aPackage='--??--', plugin_name='--??--'):
	"""Instantiates a plugin object from a package directory, returning the object.

	NOTE: it does NOT call register() for you !!!!

	- "set" specifies the subdirectory in which to find the plugin
	- this knows nothing of databases, all it does is instantiate a named plugin

	There will be a general 'gui' directory for large GUI
	components: prescritions, etc., then several others for more
	specific types: export/import filters, crypto algorithms
	guibroker, dbbroker are broker objects provided
	defaults are the default set of plugins to be loaded

	FIXME: we should inform the user about failing plugins
	"""
	# we do need brokers, else we are useless
	gb = gmGuiBroker.GuiBroker()

	# bean counting ! -> loaded plugins
	if not ('modules.%s' % aPackage) in gb.keylist():
		gb['modules.%s' % aPackage] = {}

	try:
		# use __import__() so we can dynamically calculate the module name
		mod_from_pkg = __import__("%s.%s" % (aPackage, plugin_name))
		# find name of class of plugin (must be the same as the plugin module filename)
		# 1) get module name
		plugin_module_name = mod_from_pkg.__dict__[plugin_name]
		# 2) get class name
		plugin_class = plugin_module_name.__dict__[plugin_name]
	except ImportError:
		_log.LogException ('Cannot __import__() module "%s.%s".' % (aPackage, plugin_name), sys.exc_info(), verbose=0)
		return None

	if not issubclass(plugin_class, wxNotebookPlugin):
		_log.Log(gmLog.lErr, "[%s] not a subclass of wxNotebookPlugin" % plugin_name)
		return None

	_log.Log(gmLog.lInfo, plugin_name)
	try:
		plugin = plugin_class(set = aPackage)
	except:
		_log.LogException ('Cannot open module "%s.%s".' % (aPackage, plugin_name), sys.exc_info(), verbose=0)
		return None

	return plugin
#------------------------------------------------------------------
def GetPluginLoadList(set):
	"""Get a list of plugins to load.

	1) look in database
	2) look into source directory
	 a) check for plugins.conf
	 b) scan directly
	 c) store in database
	"""
	curr_machine = _whoami.get_workplace()

	p_list, match = gmCfg.getFirstMatchingDBSet(
		machine = curr_machine,
		cookie = str(set),
		option = 'plugin load order'
	)

	# get connection for possible later use
	gb = gmGuiBroker.GuiBroker()
	db = gmPG.ConnectionPool()
	conn = db.GetConnection(service = "default")
	dbcfg = gmCfg.cCfgSQL(
		aConn = conn,
		aDBAPI = gmPG.dbapi
	)

	if p_list is not None:
		# found plugin load list for this user/this machine
		if match == 'CURRENT_USER_CURRENT_MACHINE':
			db.ReleaseConnection(service = "default")
			return p_list
		# all other cases of user/machine pairing:
		# store plugin list for the current user/current machine
		rwconn = db.GetConnection(service = "default", readonly = 0)
		dbcfg.set(
			machine = curr_machine,
			option = 'plugin load order',
			value = p_list,
			cookie = str(set),
			aRWConn = rwconn
		)
		rwconn.close()
		db.ReleaseConnection(service = "default")
		return p_list

	_log.Log(gmLog.lInfo, "No plugin load order stored in database. Trying local config file.")

	# search in plugin directory
	plugin_conf_name = os.path.join(gb['gnumed_dir'], 'wxpython', set, 'plugins.conf')
	try:
		fCfg = gmCfg.cCfgFile(aFile = plugin_conf_name)
	except:
		_log.LogException('cannot open plugin load order config file [%s]' % plugin_conf_name, sys.exc_info(), verbose=0)
		fCfg = None

	# load from file
	if fCfg is not None:
		p_list = fCfg.get("plugins", "load order")

	# parse directory directly
	if p_list is None:
		_log.Log(gmLog.lInfo, "[%s] does not contain plugin load order" % plugin_conf_name)
		search_path = os.path.join(gb['gnumed_dir'], 'wxpython', set)
		files = os.listdir(search_path)
		_log.Log(gmLog.lData, "plugin set: %s, gnumed_dir: %s" % (set, gb['gnumed_dir']))
		_log.Log(gmLog.lInfo, "scanning plugin directory [%s]" % search_path)
		_log.Log(gmLog.lData, "files found: %s" % str(files))
		p_list = []
		for file in files:
			if (re.compile ('.+\.py$').match(file)) and (file != '__init__.py'):
				p_list.append(file[:-3])
		if (len(p_list) == 0):
			_log.Log(gmLog.lErr, 'cannot find plugins by scanning plugin directory ?!?')
			db.ReleaseConnection(service = "default")
			return None

	# set for default user on this machine
	_log.Log(gmLog.lInfo, "Storing default plugin load order in database.")
	rwconn = db.GetConnection(service = "default", readonly = 0)
	dbcfg.set(
		machine = curr_machine,
		user = 'xxxDEFAULTxxx',
		option = 'plugin load order',
		value = p_list,
		cookie = str(set),
		aRWConn = rwconn
	)
	rwconn.close()

	_log.Log(gmLog.lData, "plugin load list: %s" % str(p_list))
	db.ReleaseConnection(service = "default")
	return p_list
#------------------------------------------------------------------
def UnloadPlugin (set, name):
	"""
	Unloads the named plugin
	"""
	gb = gmGuiBroker.GuiBroker ()
	plugin = gb['modules.%s' % set][name]
	plugin.unregister ()
#==================================================================
# Main
#------------------------------------------------------------------
if __name__ == '__main__':
	print "please write a unit test"

#==================================================================
# $Log: gmPlugin.py,v $
# Revision 1.25  2004-07-15 07:57:20  ihaywood
# This adds function-key bindings to select notebook tabs
# (Okay, it's a bit more than that, I've changed the interaction
# between gmGuiMain and gmPlugin to be event-based.)
#
# Oh, and SOAPTextCtrl allows Ctrl-Enter
#
# Revision 1.24  2004/07/15 06:15:55  ncq
# - fixed typo patch -> path
#
# Revision 1.23  2004/07/15 05:17:43  ncq
# - better/correct logging in GetPluginLoadList()
#
# Revision 1.22  2004/06/26 23:09:22  ncq
# - better comments
#
# Revision 1.21  2004/06/25 14:39:35  ncq
# - make right-click runtime load/drop of plugins work again
#
# Revision 1.20  2004/06/25 13:28:00  ncq
# - logically separate notebook and clinical window plugins completely
#
# Revision 1.19  2004/06/25 12:51:23  ncq
# - InstPlugin() -> instantiate_plugin()
#
# Revision 1.18  2004/06/13 22:14:39  ncq
# - extensive cleanup/comments
# - deprecate self.internal_name in favour of self.__class__.__name__
# - introduce gb['main.notebook.raised_plugin']
# - add populate_with_data()
# - DoToolbar() -> populate_toolbar()
# - remove set_widget_reference()
#
# Revision 1.17  2004/03/10 13:57:45  ncq
# - unconditionally do shadow
#
# Revision 1.16  2004/03/10 12:56:01  ihaywood
# fixed sudden loss of main.shadow
# more work on referrals,
#
# Revision 1.15  2004/03/04 19:23:24  ncq
# - moved here from pycommon
#
# Revision 1.1  2004/02/25 09:30:13  ncq
# - moved here from python-common
#
# Revision 1.68  2004/02/12 23:54:39  ncq
# - add wxBell to can_receive_focus()
# - move raise_plugin out of class gmPlugin
#
# Revision 1.67  2004/01/17 10:37:24  ncq
# - don't ShowBar() in Raise() as GuiMain.OnNotebookPageChanged()
#   takes care of that
#
# Revision 1.66  2004/01/17 09:59:02  ncq
# - enable Raise() to raise arbitrary plugins
#
# Revision 1.65  2004/01/06 23:44:40  ncq
# - __default__ -> xxxDEFAULTxxx
#
# Revision 1.64  2003/12/29 16:33:23  uid66147
# - use whoami.get_workplace()/gmPG.run_commit()
#
# Revision 1.63  2003/11/18 23:29:57  ncq
# - remove duplicate Version line
#
# Revision 1.62  2003/11/18 19:06:26  hinnef
# gmTmpPatient->gmPatient, again
#
# Revision 1.61  2003/11/17 10:56:37  sjtan
#
# synced and commiting.
#
# Revision 1.60  2003/11/09 14:26:41  ncq
# - if we have set_status_txt() do use it, too
#
# Revision 1.59  2003/11/08 10:48:36  shilbert
# - added convenience function _set_status_txt()
#
# Revision 1.58  2003/10/26 01:38:06  ncq
# - gmTmpPatient -> gmPatient, cleanup
#
# Revision 1.57  2003/09/24 10:32:54  ncq
# - whitespace cleanup
#
# Revision 1.56  2003/09/03 17:31:05  hinnef
# cleanup in GetPluginLoadList, make use of gmWhoAmI
#
# Revision 1.55  2003/07/21 20:57:42  ncq
# - cleanup
#
# Revision 1.54  2003/06/29 14:20:45  ncq
# - added TODO item
#
# Revision 1.53  2003/06/26 21:35:23  ncq
# - fatal->verbose
#
# Revision 1.52  2003/06/19 15:26:02  ncq
# - cleanup bits
# - add can_receive_focus() helper to wxNotebookPlugin()
# - in default can_receive_focus() veto() plugin activation on "no patient selected"
#
# Revision 1.51  2003/04/28 12:03:15  ncq
# - introduced internal_name() helper, adapted to use thereof
# - leaner logging
#
# Revision 1.50  2003/04/20 15:38:50  ncq
# - clean out some excessive logging
#
# Revision 1.49  2003/04/09 13:06:03  ncq
# - some cleanup
#
# Revision 1.48  2003/04/05 01:09:03  ncq
# - forgot that one in the big patient -> clinical clean up
#
# Revision 1.47  2003/02/24 12:35:55  ncq
# - renamed some function local variables to further my understanding of the code
#
# Revision 1.46  2003/02/17 16:18:29  ncq
# - fix whitespace on comments
#
# Revision 1.45  2003/02/13 12:58:05  sjtan
#
# remove unneded import.
#
# Revision 1.44  2003/02/11 18:23:39  ncq
# - removed unneeded import
#
# Revision 1.43  2003/02/11 12:27:07  sjtan
#
# suspect this is not the preferred way to get a handle on the plugin. Probably from guiBroker?
#
# Revision 1.42  2003/02/09 20:00:06  ncq
# - on notebook plugins rename Shown() to ReceiveFocus() as that's what this does, not only display itself
#
# Revision 1.41  2003/02/09 11:52:28  ncq
# - just one more silly cvs keyword
#
# Revision 1.40  2003/02/09 09:41:57  sjtan
#
# clean up new code, make it less intrusive.
#
# Revision 1.39  2003/02/07 12:47:15  sjtan
#
# using gmGuiBroker for more dynamic handler loading. (e.g. can use subclassed instances of EditAreaHandler classes).
# ~
#
# Revision 1.38  2003/02/07 08:16:16  ncq
# - some cosmetics
#
# Revision 1.37  2003/02/07 05:08:08  sjtan
#
# added few lines to hook in the handler classes from EditAreaHandler.
# EditAreaHandler was generated with editarea_gen_listener in wxPython directory.
#
# Revision 1.36  2003/01/16 14:45:04  ncq
# - debianized
#
# Revision 1.35  2003/01/16 09:18:11  ncq
# - cleanup
#
# Revision 1.34  2003/01/12 17:30:19  ncq
# - consistently return None if no plugins found by GetPluginLoadList()
#
# Revision 1.33  2003/01/12 01:45:12  ncq
# - typo, "IS None" not "== None"
#
# Revision 1.32  2003/01/11 22:03:30  hinnef
# removed gmConf
#
# Revision 1.31  2003/01/06 12:53:26  ncq
# - some cleanup bits
#
# Revision 1.30  2003/01/06 04:52:55  ihaywood
# resurrected gmDemographics.py
#
# Revision 1.29  2003/01/05 10:00:38  ncq
# - better comments
# - implement database plugin configuration loading/storing
#
# Revision 1.28  2003/01/04 07:43:55  ihaywood
# Popup menus on notebook tabs
#
# Revision 1.27  2002/11/13 09:14:17  ncq
# - document a few more todo's but don't do them before OSHCA
#
# Revision 1.26  2002/11/12 23:03:25  hherb
# further changes towards customization of plugin loading order
#
# Revision 1.25  2002/11/12 20:30:10  hherb
# Uses an optional config file in each plugin directory determining the order plugins are loaded as well as which plugins are loaded
#
# Revision 1.24  2002/09/26 13:10:43  ncq
# - silly ommitance
#
# Revision 1.23  2002/09/26 13:08:51  ncq
# - log version on import
# - TODO -> FIXME
#
# Revision 1.22  2002/09/09 00:50:28  ncq
# - return success or failure on LoadPlugin()
#
# @change log:
#	08.03.2002 hherb first draft, untested
