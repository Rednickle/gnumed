"""GNUmed data pack related widgets."""
#================================================================
__author__ = 'karsten.hilbert@gmx.net'
__license__ = 'GPL v2 or later (details at http://www.gnu.org)'

# stdlib
import logging
import sys
import urllib2 as wget

# 3rd party
import wx


# GNUmed
if __name__ == '__main__':
	sys.path.insert(0, '../../')

from Gnumed.pycommon import gmCfg2
from Gnumed.pycommon import gmCfg
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmNetworkTools
from Gnumed.business import gmSurgery
from Gnumed.wxpython import gmListWidgets
from Gnumed.wxpython import gmGuiHelpers
from Gnumed.wxpython import gmAuthWidgets


_log = logging.getLogger('gm.ui')
_cfg = gmCfg2.gmCfgData()
#================================================================
def install_data_pack(data_pack=None):

	if data_pack is None:
		return False

	_log.info('attempting installation of data pack: %s', data_pack['name'])

	gm_dbo_conn = gmAuthWidgets.get_dbowner_connection(procedure = _('installing data packs'))
	if gm_dbo_conn is None:
		msg = _('Lacking permissions to install data pack.')
		gmGuiHelpers.gm_show_error(msg, _('Installing data pack'))
		return False

	wx.BeginBusyCursor()
	verified, data = gmNetworkTools.download_data_pack (
		data_pack['pack_url'],
		md5_url = data_pack['md5_url']
	)
	wx.EndBusyCursor()
	if not verified:
		_log.error('cannot download and verify data pack: %s', data_pack['name'])
		md5_expected, md5_calculated = data
		msg = _(
			'Cannot validate data pack.\n'
			'\n'
			'  name: %s\n'
			'  URL: %s\n'
			'\n'
			'  MD5\n'
			'   calculated: %s\n'
			'   expected: %s\n'
			'   source: %s\n'
			'\n'
			'You may want to try downloading again or you\n'
			'may need to contact your administrator.'
		) % (
			data_pack['name'],
			data_pack['pack_url'],
			md5_calculated,
			md5_expected,
			data_pack['md5_url']
		)
		gmGuiHelpers.gm_show_error(msg, _('Verifying data pack'))
		return False

	data_pack['local_archive'] = data

	wx.BeginBusyCursor()
	unzip_dir = gmNetworkTools.unzip_data_pack(filename = data)
	wx.EndBusyCursor()
	if unzip_dir is None:
		msg = _(
			'Cannot unpack data pack.\n'
			'\n'
			'  name: %s\n'
			'  URL: %s\n'
			'  local: %s\n'
			'\n'
			'You may want to try downloading again or you\n'
			'may need to contact your administrator.'
		) % (
			data_pack['name'],
			data_pack['pack_url'],
			data_pack['local_archive']
		)
		gmGuiHelpers.gm_show_error(msg, _('Unpacking data pack'))
		return False

	data_pack['unzip_dir'] = unzip_dir

	wx.BeginBusyCursor()
	try:
		installed = gmNetworkTools.install_data_pack(data_pack, gm_dbo_conn)
	finally:
		wx.EndBusyCursor()

	if not installed:
		msg = _(
			'Installation of data pack failed.\n'
			'\n'
			'  name: %s\n'
			'  URL: %s\n'
			'  local: %s\n'
			'\n'
			'You may want to try downloading again or you\n'
			'may need to contact your administrator.'
		) % (
			data_pack['name'],
			data_pack['pack_url'],
			data_pack['local_archive']
		)
		gmGuiHelpers.gm_show_error(msg, _('Installing data pack'))
		return False

	msg = _(
		'Successfully installed data pack.\n'
		'\n'
		'  name: %s\n'
		'  URL: %s\n'
	) % (
		data_pack['name'],
		data_pack['pack_url']
	)
	gmGuiHelpers.gm_show_info(msg, _('Installing data pack'))

	return True
#----------------------------------------------------------------
def load_data_packs_list():

	dbcfg = gmCfg.cCfgSQL()
	dpl_url = dbcfg.get2 (
		option = u'horstspace.data_packs.url',
		workplace = gmSurgery.gmCurrentPractice().active_workplace,
		bias = 'workplace',
		default = u'http://www.gnumed.de/downloads/data/data-packs.conf'
	)

	items = []
	data = []

	dpl_fname = gmNetworkTools.download_data_packs_list(dpl_url)
	if dpl_fname is None:
		return (items, data)
	try:
		_cfg.add_file_source(source = 'data-packs', file = dpl_fname)
	except (UnicodeDecodeError):
		_log.exception("cannot read data pack list from [%s]", dpl_fname)
		return (items, data)

	packs = _cfg.get('data packs', 'data packs', source_order = [('data-packs', 'return')])
	if packs is None:
		_log.info('no data packs listed in data packs list file')
		_cfg.remove_source('data-packs')
		return (items, data)

	for pack in packs:
		_log.debug('reading pack [%s] metadata', pack)
		pack_group = u'pack %s' % pack
		name = _cfg.get(pack_group, u'name', source_order = [('data-packs', 'return')])
		pack_url = _cfg.get(pack_group, u'URL', source_order = [('data-packs', 'return')])
		md5_url = pack_url + u'.md5'
		db_min = _cfg.get(pack_group, u'minimum database version', source_order = [('data-packs', 'return')])
		converted, db_min = gmTools.input2int (
			db_min,
			# here we introduced data packs:
			#16,
			0,
			# no use looking at data packs requiring a database > the current database:
			_cfg.get(option = 'database_version')
		)
		if not converted:
			_log.error('cannot convert minimum database version [%s]', db_min)
			continue

		db_max = _cfg.get(pack_group, u'maximum database version', source_order = [('data-packs', 'return')])
		if db_max is None:
			db_max = sys.maxint
		converted, db_max = gmTools.input2int (
			db_max,
			db_min		# max version must be at least db_min
		)
		if not converted:
			_log.error('cannot convert maximum database version [%s]', db_max)
			continue

		if _cfg.get(option = 'database_version') < db_min:
			_log.error('ignoring data pack: current database version (%s) < minimum required database version (%s)', _cfg.get(option = 'database_version'), db_min)
			continue

		if _cfg.get(option = 'database_version') > db_max:
			_log.error('ignoring data pack: current database version (%s) > maximum allowable database version (%s)', _cfg.get(option = 'database_version'), db_max)
			continue

		items.append([name, u'v%s' % db_min, u'v%s' % db_max, pack_url])
		data.append ({
			'name': name,
			'pack_url': pack_url,
			'md5_url': md5_url,
			'db_min': db_min,
			'db_max': db_max
		})

	_cfg.remove_source('data-packs')
	return (items, data)
#----------------------------------------------------------------
def manage_data_packs(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	items, data = load_data_packs_list()

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _(
			'Data packs available for installation into this v%s database.\n'
		) % (
			_cfg.get(option = 'database_version')
		),
		caption = _('Showing data packs.'),
		columns = [ _('Data pack'), _('min DB'), _('max DB'), _('Source') ],
		choices = items,
		data = data,
		single_selection = True,
		can_return_empty = False,
		ignore_OK_button = True,
		left_extra_button = (
			_('&Install'),
			_('Install the selected data pack'),
			install_data_pack
		),
#		middle_extra_button=None,
#		right_extra_button=None			# configure
	)

#================================================================
# main
#----------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain()
#	from Gnumed.pycommon import gmPG2

	#--------------------------------------------------------
#	def test_generic_codes_prw():
#		gmPG2.get_connection()
#		app = wx.PyWidgetTester(size = (500, 40))
#		pw = cGenericCodesPhraseWheel(app.frame, -1)
#		#pw.set_context(context = u'zip', val = u'04318')
#		app.frame.Show(True)
#		app.MainLoop()
#	#--------------------------------------------------------
#	test_generic_codes_prw()

#================================================================