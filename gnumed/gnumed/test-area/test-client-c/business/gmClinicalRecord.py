"""GnuMed preliminary clinical patient record.

This is a clinical record object intended to let a useful
client-side API crystallize from actual use in true XP fashion.

license: GPL
"""
#============================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/test-area/test-client-c/business/Attic/gmClinicalRecord.py,v $
# $Id: gmClinicalRecord.py,v 1.3 2003-10-25 16:13:26 sjtan Exp $
__version__ = "$Revision: 1.3 $"
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"

# access our modules
import sys, os.path, string
import time
import yaml

if __name__ == "__main__":
	sys.path.append(os.path.join('..', 'python-common'))

# start logging
import gmLog
_log = gmLog.gmDefLog
if __name__ == "__main__":
	_log.SetAllLogLevels(gmLog.lData)
_log.Log(gmLog.lData, __version__)

import gmExceptions, gmPG, gmSignals, gmDispatcher
#============================================================
class gmClinicalRecord:

	# handlers for __getitem__()
	_get_handler = {}

	def __init__(self, aPKey = None):
		"""Fails if

		- no connection to database possible
		- patient referenced by aPKey does not exist
		"""
		self._backend = gmPG.ConnectionPool()

		self._ro_conn_clin = self._backend.GetConnection('historica')
		if self._ro_conn_clin is None:
			raise gmExceptions.ConstructorError, "cannot connect EMR of patient [%s] to service 'historica'" % aPKey

		self.id_patient = aPKey			# == identity.id == primary key
		if not self._pkey_exists():
			raise gmExceptions.ConstructorError, "No patient with ID [%s] in database." % aPKey

		self.__db_cache = {}

		# make sure we have a __default__ health issue
		self.id_default_health_issue = None
		if not self.__load_default_health_issue():
			raise gmExceptions.ConstructorError, "cannot activate default health issue for patient [%s]" % aPKey
		self.id_curr_health_issue = self.id_default_health_issue

		# what episode did we work on last time we saw this patient ?
		self.id_episode = None
		if not self.__load_most_recent_episode():
			raise gmExceptions.ConstructorError, "cannot activate an episode for patient [%s]" % aPKey

		# load or create current encounter
		# FIXME: this should be configurable (for explanation see the method source)
		self.encounter_soft_ttl = '2 hours'
		self.encounter_hard_ttl = '5 hours'
		self.id_encounter = None

		# register backend notification interests
		# (keep this last so we won't hang on threads when
		#  failing this constructor for other reasons ...)
		if not self._register_interests():
			raise gmExceptions.ConstructorError, "cannot register signal interests"

		_log.Log(gmLog.lData, 'Instantiated clinical record for patient [%s].' % self.id_patient)
	#--------------------------------------------------------
	def cleanup(self):
		_log.Log(gmLog.lData, 'cleaning up after clinical record for patient [%s]' % self.id_patient)
		sig = "%s:%s" % (gmSignals.item_change_db(), self.id_patient)
		self._backend.Unlisten(service = 'historica', signal = sig, callback = self._clin_item_modified)
		sig = "%s:%s" % (gmSignals.health_issue_change_db(), self.id_patient)
		self._backend.Unlisten(service = 'historica', signal = sig, callback = self._health_issues_modified)

		self._backend.Unlisten(service = 'historica', signal = gmSignals.allergy_add_del_db(), callback = self._allergy_added_deleted)

		self._backend.ReleaseConnection('historica')
	#--------------------------------------------------------
	# internal helper
	#--------------------------------------------------------
	def _pkey_exists(self):
		"""Does this primary key exist ?

		- true/false/None
		"""
		ro_conn_demo = self._backend.GetConnection('personalia')
		if ro_conn_demo is None:
			_log.Log(gmLog.lErr, "cannot connect to service 'personalia' to check for patient [%s] existence" % self.id_patient)
			return None
		curs = ro_conn_demo.cursor()
		cmd = "select exists(select id from identity where id = %s)"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			self._backend.ReleaseConnection('personalia')
			_log.Log(gmLog.lData, 'unable to check for patient [%s] existence' % self.id_patient)
			return None
		result = curs.fetchone()[0]
		curs.close()
		self._backend.ReleaseConnection('personalia')
		return result
	#--------------------------------------------------------
	# messaging
	#--------------------------------------------------------
	def _register_interests(self):
		# backend
		if not self._backend.Listen(service = 'historica', signal = gmSignals.allergy_add_del_db(), callback = self._allergy_added_deleted):
			return None
		if not self._backend.Listen(service = 'historica', signal = gmSignals.health_issue_change_db(), callback = self._health_issues_modified):
			return None
		sig = "%s:%s" % (gmSignals.item_change_db(), self.id_patient)
		if not self._backend.Listen(service = 'historica', signal = sig, callback = self._clin_item_modified):
			return None
		return 1
	#--------------------------------------------------------
	def _allergy_added_deleted(self):
		curs = self._ro_conn_clin.cursor()
		# did number of allergies change for our patient ?
		cmd = "select count(id) from v_i18n_patient_allergies where id_patient=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lData, 'cannot check for added/deleted allergies, assuming addition/deletion did occurr')
			# error: invalidate cache
			del self.__db_cache['allergies']
			# and tell others
			gmDispatcher.send(signal = gmSignals.allergy_updated(), sender = self.__class__.__name__)
			return 1
		result = curs.fetchone()
		curs.close()
		# not cached yet
		try:
			nr_cached_allergies = len(self.__db_cache['allergies'])
		except KeyError:
			gmDispatcher.send(signal = gmSignals.allergy_updated(), sender = self.__class__.__name__)
			return 1
		# no change for our patient ...
		if result == nr_cached_allergies:
			return 1
		# else invalidate cache
		del self.__db_cache['allergies']
		gmDispatcher.send(signal = gmSignals.allergy_updated(), sender = self.__class__.__name__)
		return 1
	#--------------------------------------------------------
	def _health_issues_modified(self):
		_log.Log(gmLog.lData, 'DB: clin_health_issue modification')
		try:
			del self.__db_cache['health issues']
		except KeyError:
			pass
		gmDispatcher.send(signal = gmSignals.health_issue_updated(), sender = self.__class__.__name__)
		return 1
	#--------------------------------------------------------
	def _clin_item_modified(self):
		_log.Log(gmLog.lData, 'DB: clin_root_item modification')
	#--------------------------------------------------------
	# __setitem__ handling
	#--------------------------------------------------------
	def __setitem__(self, item=None, value=None):
		if item == 'new clinical note':
			return self.create_clinical_note(value)
		_log.Log(gmLog.lWarn, "don't know how to set item [%s]" % item)
		raise KeyError, "don't know how to set item [%s]" % item
	#--------------------------------------------------------
	def create_clinical_note(self, note = None):
		if note is None:
			_log.Log(gmLog.lInfo, 'will not create empty clinical note')
			return 1
		rwconn = self._backend.GetConnection('historica', readonly=0)
		rwcurs = rwconn.cursor()
		cmd = "insert into clin_note(id_encounter, id_episode, narrative) values (%s, %s, %s)"
		if not gmPG.run_query(rwcurs, cmd, self.id_encounter, self.id_episode, note):
			rwcurs.close()
			rwconn.close()
			_log.Log(gmLog.lErr, 'cannot create clinical note (episode %d, encounter %d)' % (self.id_episode, self,id_encounter))
			return None
		rwconn.commit()
		rwcurs.close()
		rwconn.close()
		return 1
	#--------------------------------------------------------
	# __getitem__ handling
	#--------------------------------------------------------
	def __getitem__(self, aVar = None):
		"""Return any attribute if known how to retrieve it.
		"""
		try:
			return gmClinicalRecord._get_handler[aVar](self)
		except KeyError:
			_log.LogException('Missing get handler for [%s]' % aVar, sys.exc_info())
			return None
	#--------------------------------------------------------
	def _get_text_dump(self):
		# don't know how to invalidate this by means of
		# a notify without catching notifies from *all*
		# child tables, the best solution would be if
		# inserts in child tables would also fire triggers
		# of ancestor tables, but oh well,
		# until then the text dump will not be cached ...
		try:
			return self.__db_cache['text dump']
		except KeyError:
			pass
		# not cached so go get it
		fields = [
			'age',
			"to_char(modified_when, 'YYYY-MM-DD @ HH24:MI') as modified_when",
			'modified_by',
			"case is_modified when false then '%s' else '%s' end as modified_string" % (_('original entry'), _('modified entry')),
			'id_item',
			'id_encounter',
			'id_episode',
			'id_health_issue',
			'src_table'
		]
		cmd = "select %s from v_patient_items where id_patient=%%s order by src_table, age" % string.join(fields, ', ')
		curs = self._ro_conn_clin.cursor()
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load item links for patient [%s]' % self.id_patient)
			return None
		rows = curs.fetchall()
		view_col_idx = gmPG.get_col_indices(curs)
		# aggregate by src_table for item retrieval
		items_by_table = {}
		for item in rows:
			src_table = item[view_col_idx['src_table']]
			id_item = item[view_col_idx['id_item']]
			if not items_by_table.has_key(src_table):
				items_by_table[src_table] = {}
			items_by_table[src_table][id_item] = item
		# get mapping for issue/episode IDs
		issue_map = self._get_health_issue_names()
		if issue_map is None:
			issue_map = {}
		episode_map = self._get_episode_names()
		if episode_map is None:
			episode_map = {}
		emr_data = {}
		# get item data from all source tables
		for table_name in items_by_table.keys():
			item_ids = items_by_table[table_name].keys()
			# we don't know anything about the columns of
			# the source tables but, hey, this is a dump
			cmd = "select * from %s where id in %%s order by modified_when" % table_name
			if not gmPG.run_query(curs, cmd, (tuple(item_ids),)):
				_log.Log(gmLog.lErr, 'cannot load items from table [%s]' % table_name)
				# skip this table
				continue
			rows = curs.fetchall()
			table_col_idx = gmPG.get_col_indices(curs)
			curs.close()
			# format per-table items
			for row in rows:
				id_item = row[table_col_idx['id']]
				view_row = items_by_table[table_name][id_item]
				age = view_row[view_col_idx['age']]
				# format metadata
				try:
					episode_name = episode_map[view_row[view_col_idx['id_episode']]]
				except:
					episode_name = view_row[view_col_idx['id_episode']]
				try:
					issue_name = issue_map[view_row[view_col_idx['id_health_issue']]]
				except:
					issue_name = view_row[view_col_idx['id_health_issue']]

				if not emr_data.has_key(age):
					emr_data[age] = []

				emr_data[age].append(
					_('%s: encounter (%s) with "%s"') % (
						view_row[view_col_idx['modified_when']],
						view_row[view_col_idx['id_encounter']],
						view_row[view_col_idx['modified_by']]
					)
				)
				emr_data[age].append(_('health issue: %s') % issue_name)
				emr_data[age].append(_('episode     : %s') % episode_name)
				# format table specific data columns
				# - ignore those, they are metadata
				cols2ignore = [
					'pk_audit', 'row_version', 'modified_when', 'modified_by',
					'pk_item', 'id', 'id_encounter', 'id_episode'
				]
				col_data = []
				for col_name in table_col_idx.keys():
					if col_name in cols2ignore:
						continue
					emr_data[age].append(">>> %s <<<" % col_name)
					emr_data[age].append(row[table_col_idx[col_name]])
				emr_data[age].append(">>> %s from table %s <<<" % (
					view_row[view_col_idx['modified_string']],
					table_name
				))
		return emr_data
	#--------------------------------------------------------
	def _get_patient_ID(self):
		return self.id_patient
	#--------------------------------------------------------
	def _get_allergies(self):
		"""Return our rows from v_i18n_patient_allergies."""
		try:
			return self.__db_cache['allergies']
		except:
			pass
		self.__db_cache['allergies'] = []
		curs = self._ro_conn_clin.cursor()
		cmd = "select * from v_i18n_patient_allergies where id_patient=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load allergies for patient [%s]' % self.id_patient)
			del self.__db_cache['allergies']
			return None
		rows = curs.fetchall()
		curs.close()
		self.__db_cache['allergies'] = rows
		#<DEBUG>
		_log.Data("gmClinicalRecord.db_cache['allergies']: %s" % str(rows))
		#</DEBUG>
		return self.__db_cache['allergies']
	#--------------------------------------------------------
	def _get_allergy_names(self):
		data = []
		try:
			self.__db_cache['allergies']
		except KeyError:
			if self._get_allergies() is None:
				# remember: empty list will return false
				# even though this is what we get with no allergies
				_log.Log(gmLog.lErr, "Could not load allergies")
				return []
		for allergy in self.__db_cache['allergies']:
			# filter out sensitivities
			if allergy[15] == 2:
				continue
			tmp = {}
			# FIXME: this should be accessible by col name, not position
			tmp['id'] = allergy[0]
			# do we know the allergene ?
			if allergy[10] not in [None, '']:
				tmp['name'] = allergy[10]
			# no but the substance
			else:
				tmp['name'] = allergy[6]
			data.append(tmp)
		return data
	#--------------------------------------------------------
	def _get_allergies_list(self):
		"""Return list of IDs in v_i18n_patient_allergies for this patient."""
		try:
			return self.__db_cache['allergy IDs']
		except KeyError:
			pass
		self.__db_cache['allergy IDs'] = []
		curs = self._ro_conn_clin.cursor()
		cmd = "select id from v_i18n_patient_allergies where id_patient=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load list of allergies for patient [%s]' % self.id_patient)
			del self.__db_cache['allergy IDs']
			return None
		rows = curs.fetchall()
		curs.close()
		for row in rows:
			self.__db_cache['allergy IDs'].extend(row)
		return self.__db_cache['allergy IDs']
	#--------------------------------------------------------
	def _get_episode_names(self):
		try:
			return self.__db_cache['episode names']
		except KeyError:
			pass
		self.__db_cache['episode names'] = {}
		curs = self._ro_conn_clin.cursor()
		cmd = "select id_episode, episode from v_patient_episodes where id_patient=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load episode names for patient [%s]' % self.id_patient)
			del self.__db_cache['episode names']
			return None
		rows = curs.fetchall()
		col_idx = gmPG.get_col_indices(curs)
		curs.close()
		idx_id = col_idx['id_episode']
		idx_name = col_idx['episode']
		for row in rows:
			self.__db_cache['episode names'][row[idx_id]] = row[idx_name]
		return self.__db_cache['episode names']
	#--------------------------------------------------------
	def _get_health_issues(self):
		try:
			return self.__db_cache['health issues']
		except KeyError:
			pass
		self.__db_cache['health issues'] = {}
		curs = self._ro_conn_clin.cursor()
		cmd = "select id, description from clin_health_issue where id_patient=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load health issues for patient [%s]' % self.id_patient)
			del self.__db_cache['health issues']
			return None
		rows = curs.fetchall()
		col_idx = gmPG.get_col_indices(curs)
		curs.close()
		idx_id = col_idx['id']
		idx_name = col_idx['description']
		for row in rows:
			self.__db_cache['health issues'][row[idx_id]] = row[idx_name]
		return self.__db_cache['health issues']
	#--------------------------------------------------------
	def _get_health_issue_names(self):
		try:
			return self.__db_cache['health issue names']
		except KeyError:
			pass
		self.__db_cache['health issue names'] = {}
		curs = self._ro_conn_clin.cursor()
		cmd = "select id, description from clin_health_issue where id_patient=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load health issue names for patient [%s]' % self.id_patient)
			del self.__db_cache['health issue names']
			return None
		rows = curs.fetchall()
		col_idx = gmPG.get_col_indices(curs)
		curs.close()
		idx_id = col_idx['id']
		idx_name = col_idx['description']
		for row in rows:
			self.__db_cache['health issue names'][row[idx_id]] = row[idx_name]
		return self.__db_cache['health issue names']
	#--------------------------------------------------------
	def _get_vaccination_status(self):
		try:
			return self.__db_cache['vaccination status']
		except KeyError:
			pass
		self.__db_cache['vaccination status'] = {}
		tmp = {}

		# need to actually fetch data:
		curs = self._ro_conn_clin.cursor()

		# - some vaccinations the patient may have never had
		cmd = """
select distinct on (description) description
from vacc_indication
where description not in (
	select indication
	from v_patient_vaccinations
	where id_patient=%s
)"""
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load vaccination indications')
			del self.__db_cache['vaccination status']
			return None
		rows = curs.fetchall()
		tmp['missing'] = []
		for row in rows:
			tmp['missing'].append(row[0])

		# - some will be incomplete but not due currently
		cmd = """
select distinct on (vpv.indication) vpv.indication
from v_patient_vaccinations vpv
where
	id_patient=%s
		and
	(select age(dob) from v_basic_person where id=%s) not between a and b
"""


		curs.close()

		return self.__db_cache['vaccination status']
	#--------------------------------------------------------
	# set up handler map
	_get_handler['patient ID'] = _get_patient_ID
#	_get_handler['allergy IDs'] = _get_allergies_list
	_get_handler['allergy names'] = _get_allergy_names
	_get_handler['allergies'] = _get_allergies
	_get_handler['text dump'] = _get_text_dump
	_get_handler['episode names'] = _get_episode_names
	_get_handler['health issues'] = _get_health_issues
	_get_handler['health issue names'] = _get_health_issue_names
	_get_handler['vaccination status'] = _get_vaccination_status
	_get_handler['immunisation status'] = _get_vaccination_status
	_get_handler['immunization status'] = _get_vaccination_status
	#------------------------------------------------------------------
	# health issue related helpers
	#------------------------------------------------------------------
	def __load_default_health_issue(self):
		self.id_default_health_issue = self._create_health_issue()
		if self.id_default_health_issue is None:
			_log.Log(gmLog.lErr, 'cannot load default health issue for patient [%s]' % self.id_patient)
			return None
		return 1
	#------------------------------------------------------------------
	def _create_health_issue(self, health_issue_name = '__default__'):
		curs = self._ro_conn_clin.cursor()
		cmd = "select id from clin_health_issue where id_patient=%s and description=%s"
		if not gmPG.run_query(curs, cmd, self.id_patient, health_issue_name):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot check if health issue [%s] exists for patient [%s]' % (health_issue_name, self.id_patient))
			return None
		row = curs.fetchone()
		curs.close()
		# issue exists already
		if row is not None:
			return row[0]
		# issue does not exist yet so create it
		_log.Log(gmLog.lData, "health issue [%s] does not exist for patient [%s]" % (health_issue_name, self.id_patient))
		rw_conn = self._backend.GetConnection('historica', readonly = 0)
		rw_curs = rw_conn.cursor()
		cmd = "insert into clin_health_issue (id_patient, description) values (%s, %s)"
		if not gmPG.run_query(rw_curs, cmd, self.id_patient, health_issue_name):
			rw_curs.close()
			rw_conn.close()
			_log.Log(gmLog.lErr, 'cannot insert health issue [%s] for patient [%s]' % (health_issue_name, self.id_patient))
			print "insert"
			return None
		# get ID of insertion
		cmd = "select currval('clin_health_issue_id_seq')"
		if not gmPG.run_query(rw_curs, cmd):
			rw_curs.close()
			rw_conn.close()
			_log.Log(gmLog.lErr, 'cannot obtain id of last health issue insertion')
			print "find currval"
			return None
		id_issue = rw_curs.fetchone()[0]
		# and commit our work
		rw_conn.commit()
		rw_curs.close()
		rw_conn.close()
		_log.Log(gmLog.lData, 'inserted [%s] issue with ID [%s] for patient [%s]' % (health_issue_name, id_issue, self.id_patient))
		
		return id_issue
	#------------------------------------------------------------------
	# episode related helpers
	#------------------------------------------------------------------
	def __load_most_recent_episode(self):
		# check if there's an active episode
		curs = self._ro_conn_clin.cursor()
		cmd = "select id_episode from last_act_episode where id_patient=%s limit 1"
		if not gmPG.run_query(curs, cmd, self.id_patient):
			curs.close()
			_log.Log(gmLog.lErr, 'cannot load last active episode for patient [%s]' % self.id_patient)
			return None
		row = curs.fetchone()
		curs.close()
		# no: should only happen in new patients
		if row is None:
			# try to set one to active or create default one
			if not self._set_active_episode():
				_log.Log(gmLog.lErr, 'cannot activate default episode for patient [%s]' % self.id_patient)
				return None
		else:
			self.id_episode = row[0]
		return 1
	#------------------------------------------------------------------
	def _set_active_episode(self, episode_name = '__default__'):
		ro_curs = self._ro_conn_clin.cursor()
		# does this episode exist at all ?
		# (else we can't activate it in the first place)
		cmd = "select id_episode from v_patient_episodes where id_patient=%s and episode=%s limit 1"
		if not gmPG.run_query(ro_curs, cmd, self.id_patient, episode_name):
			ro_curs.close()
			_log.Log(gmLog.lErr, 'cannot load episode [%s] for patient [%s]' % (episode_name, self.id_patient))
			return None
		row = ro_curs.fetchone()
		ro_curs.close()
		# no
		if row is None:
			# if __default__ then create it
			if episode_name == '__default__':
				id_episode = self._create_episode()
				# unless that fails
				if id_episode is None:
					return None
			# else fail
			else:
				_log.Log(gmLog.lErr, 'patient [%s] has no episode [%s]' % (self.id_patient, episode_name))
				return None
		# yes
		else:
			id_episode = row[0]

		# eventually activate it
		rw_conn = self._backend.GetConnection('historica', readonly = 0)
		rw_curs = rw_conn.cursor()
		# delete old entry
		cmd = "delete from last_act_episode where id_patient=%s"
		if not gmPG.run_query(rw_curs, cmd, self.id_patient):
			_log.Log(gmLog.lWarn, 'cannot delete last active episode entry for patient [%s]' % (self.id_patient))
			# try continuing anyways
		cmd = "insert into last_act_episode (id_episode, id_patient) values (%s, %s)"
		if not gmPG.run_query(rw_curs, cmd, id_episode, self.id_patient):
			_log.Log(gmLog.lErr, 'cannot activate episode [%s] for patient [%s]' % (id_episode, self.id_patient))
			rw_curs.close()
			rw_conn.close()
			return None
		# seems we succeeded
		rw_conn.commit()
		rw_curs.close()
		rw_conn.close()
		self.id_episode = id_episode
		return 1
	#------------------------------------------------------------------
	def _create_episode(self, episode_name = '__default__'):
		ro_curs = self._ro_conn_clin.cursor()
		# anything to do ?
		cmd = "select id_episode from v_patient_episodes where id_patient=%s and episode=%s limit 1"
		if not gmPG.run_query(ro_curs, cmd, self.id_patient, episode_name):
			ro_curs.close()
			_log.Log(gmLog.lErr, 'cannot check if episode [%s] exists for patient [%s]' % (episode_name, self.id_patient))
			return None
		row = ro_curs.fetchone()
		ro_curs.close()
		# episode already exists
		if row is not None:
			return row[0]
		# episode does not exist yet so create it
		rw_conn = self._backend.GetConnection('historica', readonly = 0)
		if rw_conn is None:
			return None
		rw_curs = rw_conn.cursor()
		# for now new episodes belong to the __default__ health issue
		cmd = "insert into clin_episode (id_health_issue, description) values (%s, %s)"
		if not gmPG.run_query(rw_curs, cmd, self.id_default_health_issue, episode_name):
			rw_curs.close()
			rw_conn.close()
			_log.Log(gmLog.lErr, 'cannot insert episode [%s] for patient [%s]' % (episode_name, self.id_patient))
			return None
		# get id for it
		cmd = "select currval('clin_episode_id_seq')"
		if not gmPG.run_query(rw_curs, cmd):
			rw_curs.close()
			rw_conn.close()
			_log.Log(gmLog.lErr, 'cannot obtain id of last episode insertion')
			return None
		id_episode = rw_curs.fetchone()[0]
		# and commit our work
		rw_conn.commit()
		rw_curs.close()
		rw_conn.close()
		return id_episode
	#------------------------------------------------------------------
	# encounter related helpers
	#------------------------------------------------------------------
	def attach_to_encounter(self, anID = None, forced = None, comment = 'affirmed'):
		"""Try to attach to an encounter.
		"""
		self.id_encounter = None

		# if forced to ...
		if forced:
			# ... create a new encounter and attach to that
			if anID is None:
				self.id_encounter = self.__insert_encounter()
				if self.id_encounter is None:
					return -1, ''
				else:
					return 1, ''
			# ... attach to a particular encounter
			else:
				self.id_encounter = anID
				if not self.__affirm_current_encounter(comment):
					return -1, ''
				else:
					return 1, ''

		# else auto-search for encounter and attach if necessary
		ro_curs = self._ro_conn_clin.cursor()
		if anID is None:
			# 1) very recent encounter recorded (that we always consider current) ?
			cmd = "select id_encounter, started, last_affirmed, \"comment\" from curr_encounter where id_patient=%s and now() - last_affirmed < %s::interval limit 1"
			if not gmPG.run_query(ro_curs, cmd, self.id_patient, self.encounter_soft_ttl):
				ro_curs.close()
				_log.Log(gmLog.lErr, 'cannot access current encounter table')
				return -1, ''
			row = ro_curs.fetchone()
			# yes, so update and return that
			if row is not None:
				ro_curs.close()
				self.id_encounter = row[0]
				if not self.__affirm_current_encounter(comment):
					return -1, ''
				else:
					return 1, ''

			# 2) encounter recorded that's fairly recent ?
			cmd = "select id_encounter, started, last_affirmed, \"comment\" from curr_encounter where id_patient=%s and now() - last_affirmed < %s::interval limit 1"
			if not gmPG.run_query(ro_curs, cmd, self.id_patient, self.encounter_hard_ttl):
				ro_curs.close()
				_log.Log(gmLog.lErr, 'cannot access current encounter table')
				return -1, ''
			row = ro_curs.fetchone()
			ro_curs.close()
			# ask user what to do about it
			if row is not None:
				data = {
					'ID': row[0],
					'started': row[1],
					'affirmed': row[2],
					'comment': row[3]
				}
				return 0, data

			# 3) no encounter active or timed out, so create new one
			self.id_encounter = self.__insert_encounter(comment)
			if self.id_encounter is None:
				return -1, ''
			else:
				return 1, ''
		else:
			_log.Log(gmLog.lErr, 'invalid argument combination: forced=false + anID=[%d]' % anID)
			return -1, ''
	#------------------------------------------------------------------
	def __insert_encounter(self, aComment = 'created'):
		"""Insert a new encounter.
		"""
		rw_conn = self._backend.GetConnection('historica', readonly = 0)
		if rw_conn is None:
			_log.Log(gmLog.lErr, 'cannot connect to service [historica]')
			return None
		rw_curs = rw_conn.cursor()
		# delete old entry if any
		cmd = "delete from curr_encounter where id_patient=%s"
		if not gmPG.run_query(rw_curs, cmd, self.id_patient):
			_log.Log(gmLog.lErr, 'cannot delete curr_encounter entry for patient [%s]' % self.id_patient)
		# insert new encounter
		# FIXME: we don't deal with location/provider yet
		cmd = "insert into clin_encounter(id_location, id_provider) values(-1, -1)"
		if not gmPG.run_query(rw_curs, cmd):
			_log.Log(gmLog.lErr, 'cannot insert new encounter for patient [%s]' % self.id_patient)
			rw_curs.close()
			rw_conn.close()
			return None
		# get ID
		cmd = "select currval('clin_encounter_id_seq')"
		if not gmPG.run_query(rw_curs, cmd):
			_log.Log(gmLog.lErr, 'cannot obtain id of last encounter insertion')
			rw_curs.close()
			rw_conn.close()
			return None
		id_encounter = rw_curs.fetchone()[0]
		# and record as currently active encounter
		cmd = "insert into curr_encounter (id_encounter, id_patient, \"comment\") values (%s, %s, %s)"
		if not gmPG.run_query(rw_curs, cmd, id_encounter, self.id_patient, aComment):
			_log.Log(gmLog.lErr, 'cannot record currently active encounter for patient [%s]' % self.id_patient)
			rw_curs.close()
			rw_conn.close()
			return None
		# we succeeded apparently
		rw_conn.commit()
		rw_curs.close()
		rw_conn.close()
		return 1
	#------------------------------------------------------------------
	def __affirm_current_encounter(self, aComment = 'affirmed'):
		"""Update internal comment and time stamp on curr_encounter row.
		"""
		rw_conn = self._backend.GetConnection('historica', readonly = 0)
		if rw_conn is None:
			_log.Log(gmLog.lWarn, 'cannot connect to service [historica]')
			return None
		rw_curs = rw_conn.cursor()
		cmd = "update curr_encounter set comment=%s where id_patient=%s and id_encounter=%s"
		if not gmPG.run_query(rw_curs, cmd, aComment, self.id_patient, self.id_encounter):
			_log.Log(gmLog.lErr, 'cannot reaffirm encounter')
			rw_curs.close()
			rw_conn.close()
			return None
		rw_conn.commit()
		rw_curs.close()
		rw_conn.close()
		return 1
	#------------------------------------------------------------------
	# trial: allergy panel
	#------------------------------------------------------------------
	def create_allergy(self, map):
		"""tries to add allergy to database."""
		rw_conn = self._backend.GetConnection('historica', readonly = 0)
		if rw_conn is None:
			_log.Log(gmLog.lErr, 'cannot connect to service [historica]')
			return None
		rw_curs = rw_conn.cursor()
		# FIXME: id_type hardcoded, not reading checkbox states (allergy or sensitivity)
		cmd = """
insert into
allergy(id_type, id_encounter, id_episode,  substance, reaction, definite)
values (%s, %s, %s, %s, %s, %s)
"""
		gmPG.run_query (rw_curs, cmd, 1, self.id_encounter, self.id_episode, map["substance"], map["reaction"], map["definite"])
		rw_curs.close()
		rw_conn.commit()
		rw_conn.close()

		return 1

	#-----------------------------------------------------------------------
	#This is basic Observer pattern, or  model-view pattern
	#----------------------------------------------------------------------
	# use the more general gmDispatcher
#	def getObservers(self):
#		if not self.__dict__.has_key('observers'):
#			self.observers = []
#		list = []
#		list.extend(self.observers)
#		return list
	
#	def addObserver(self, observer):
#		if observer not in self.getObservers():
#			self.observers.append(observer)
		
#	def notifyObservers(self):
#		for observer in self.getObservers():
#			observer.modelChanged(self)


			
	#------------------------------------------------------------------
	# yaml input and output conversions
	#------------------------------------------------------------------

	def get_yaml_string(self, keys, map):
		l = ["---"]
		for k in keys:
			l.append(  ''.join( ("  ", k ,":",  str(map[k]) ) ) )
		return 	"\n".join(l) 
	
	def load_yaml_collection(self, cmd, params):
		"""loads  a yaml serialized field for a patient into a list, a map, and a storage ordered map.items()"""
		(curs, conn) = self._runQuery(schema = 'historica',  cmd = cmd, params = self.id_patient)
		l = curs.fetchall()
		_log.Log( gmLog.lData,  "retrieved %s" % str(l) )
		curs.close()
		seq_with_id = []
		for x in l:
			try :
				id, result = x[0],  list(yaml.load( x[1] ))
				seq_with_id.append( (id, result[0]) )
			except:
				print sys.exc_info()[0], sys.exc_info()[1]
				print "trying to load ", x[1]
			
		return  seq_with_id


	#-----------------------------------------------------------------
	# trial past history, use yaml serialization to store ui dependent info in text field
	#----------------------------------------------------------------
	
	def _getLaterality(self, map):
		if map.get('both', 0) == 1:
			return 'both'
		if map.get('right', 0) == 1:
			return 'right'
		if map.get('left', 0) == 1:
			return 'left'
		if map.get('none',0) == 1:
			return 'none'
	
	def _putLaterality(self, map):
		laterality = map.get('laterality', "none")
		map.update( {'both' : laterality == 'both', 
			     'left':  laterality == 'left',
			     'right': laterality == 'right',
			     'none': laterality == 'none' } )
			
	def _getNotes( self, map):
		s1, s2 = map['notes1'].strip(), map['notes2'].strip()
		
		if s1 == "" or s2 == "":
			return "".join( ('"',s1, s2, '"') )
		return  "|".join( (s1, s2)  )

	def _putNotes( self, map):
		list =  map['notes'].split('|')
		if len(list) == 1:
			map['notes1'] , map['notes2'] = list[0], ''
		else:
			map['notes1'] , map['notes2'] = list[0], list[1]
			
		

	def _putAge( self, map):
		pass
		#map['age'] = map['year'] - self._getBirthYear()
		
	def _getBirthDate(self):
		if not self.__dict__.has_key('birthdate') :
			(curs, conn) = self._runQuery(cmd='select dob from v_basic_person where id = %d', params = self.id_patient)
			self.birthdate = curs.fetchone()[0]
			curs.close()
		return self.birthdate	

	def _getBirthYear(self):
		"""need patient info for birth year"""
		return time.localtime(self._getBirthDate())[0]

	def _getCurrentAge(self):
		"""need patient info and current for current age"""
		return time.localtime()[0] - self._getBirthYear()

	def _runQuery(self,schema = 'personalia'  , readonly = 1,  cmd = 'select %d', params = 1):
		conn = self._backend.GetConnection(schema, readonly )
		ro_curs = conn.cursor()

		#<DEBUG>
		print  "executing ", cmd % params
		#</DEBUG>
		_log.Log(gmLog.lData,  "executing ", cmd % params )

		ro_curs.execute(cmd % params)
		return (ro_curs, conn)
		

	def _getYear( self, map):
		y =  int(map.get( 'year','0'))
	
		if  y > 0:
			return y

		age = int(map.get('age', '0'))
		if  age > 0:
			return self._getBirthYear() + map['age']

		return ''

	def _history_input_to_store_map(self, map):
		map['laterality'] = self._getLaterality( map)
		map['notes'] = self._getNotes(map)
		map['year'] = self._getYear( map)

	def _history_store_to_input_map(self, map):
		self._putLaterality(map)
		self._putAge(map)
		self._putNotes(map)
	
	def create_history(self, map):
		# last output 23/10/2003
		#{ past history : ['active', 'age', 'both', 'condition', 'confidential', 'left', 'notes1', 'notes2', 'operation', 'progress', 'right', 'significant', 'year'] }
		self._history_input_to_store_map( map)
		description = self.get_yaml_string(self._get_history_storage_keys(), map) 
		cmd="insert into clin_history ( narrative, id_type, id_episode, id_encounter) values('%s', 1, %d, %d )" 
		params =( description, self.id_episode, self.id_encounter )
		conn = self._backend.GetConnection('historica', readonly = 0)
		curs = conn.cursor()
		curs.execute( cmd % params)
		curs.execute("select currval('clin_history_id_seq')")
		[id] = curs.fetchone()
		conn.commit()
		curs.close()
		self._add_to_local_history( id, map)
			
	
	def _add_to_local_history(self, id, map):
		self.past.append( (id, map) )
		gmDispatcher.send(gmSignals.clin_history_updated())


	def update_history( self,map,  ix) :
			cmd = "update clin_history set  narrative='%s', id_type= 1, id_episode=%d, id_encounter=%d where id = %d"
			
	def _get_history_storage_keys(self):
		return [ 'significant', 'condition', 'active', 'year' , 'laterality', 'operation', 'confidential', 'notes' ]
	
	
	def get_all_history(self):
		"""gets the history from the local store , else fetches it with load_past_history"""
		if not self.__dict__.has_key('past'):
			self.load_all_history()

		return self.past
	
	def load_all_history(self):
		"""loads the past history for the patient"""
		list = self.load_yaml_collection( cmd="""select h.id, h.narrative from clin_history h, 
									clin_episode e , 
									clin_health_issue hi 
									where  h.id_episode = e.id and 
									e.id_health_issue = hi.id and 
									hi.id_patient = %d
									""", params = self.id_patient)
		for (id, map) in list:
			self._history_store_to_input_map(map)
		
		self.past = list
									
		#self.notifyObservers()

	
	def filter_history(self, key, range, list = [], includeAsDefault = 0):
		print "filtering with ", key, " in ", range
		
		if list == []:
			list = self.get_all_history()
		l = []
		for id, map in list:
			print "checking ", map.get(key, None) 
			if map.get(key , None) in range:
				l.append( (id,map) )
			elif includeAsDefault  and not map.has_key(key): 
				l.append( (id,map) )
		return l

	def get_accepted_history(self):
		return self.filter_history( 'rejected', range=[0], includeAsDefault=1 )
		
	
	def get_active_history(self, active = 1 , list = []):
		if list == [] :
			list = self.get_accepted_history()

		return self.filter_history( 'active', [active], list)
		
	def get_significant_history( self, significant = 1, list = []):
		if list == [] :
			list = self.get_accepted_history()

		return self.filter_history( 'significant', [significant], list, includeAsDefault = 0)

	def get_significant_past_history( self ):
		return self.get_significant_history( list = self.get_active_history( active = 0) )

	def set_rejected_history(self, index, rejected = 1):
		list = self.get_accepted_history()
		if index >= len( list):
			return
		(id, map ) = list[index]
		map['reject'] = rejected
		

	def get_history_fields(self, index):
		"""converts to fields for display"""
		map = self.get_accepted_history()[index]
		self._putLaterality(map)
		self._putAge(map)
		self._putNotes(map)
		return map
	
		
	
#============================================================
# main
#------------------------------------------------------------
if __name__ == "__main__":
	record = gmClinicalRecord(aPKey = 1)
	dump = record['text dump']
	if dump is not None:
		keys = dump.keys()
		keys.sort()
		for aged_line in keys:
			for line in dump[aged_line]:
				print line
	import time
	time.sleep(3)
	del record
#============================================================
# $Log: gmClinicalRecord.py,v $
# Revision 1.3  2003-10-25 16:13:26  sjtan
#
# past history , can add  after selecting patient.
#
# Revision 1.2  2003/10/25 08:29:40  sjtan
#
# uses gmDispatcher to send new currentPatient objects to toplevel gmGP_ widgets. Proprosal to use
# yaml serializer to store editarea data in  narrative text field of clin_root_item until
# clin_root_item schema stabilizes.
#
# Revision 1.1  2003/10/23 06:02:38  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.36  2003/10/19 12:12:36  ncq
# - remove obsolete code
# - filter out sensitivities on get_allergy_names
# - start get_vacc_status
#
# Revision 1.35  2003/09/30 19:11:58  ncq
# - remove dead code
#
# Revision 1.34  2003/07/19 20:17:23  ncq
# - code cleanup
# - add cleanup()
# - use signals better
# - fix get_text_dump()
#
# Revision 1.33  2003/07/09 16:20:18  ncq
# - remove dead code
# - def_conn_ro -> ro_conn_clin
# - check for patient existence in personalia, not historica
# - listen to health issue changes, too
# - add _get_health_issues
#
# Revision 1.32  2003/07/07 08:34:31  ihaywood
# bugfixes on gmdrugs.sql for postgres 7.3
#
# Revision 1.31  2003/07/05 13:44:12  ncq
# - modify -> modified
#
# Revision 1.30  2003/07/03 15:20:55  ncq
# - lots od cleanup, some nice formatting for text dump of EMR
#
# Revision 1.29  2003/06/27 22:54:29  ncq
# - improved _get_text_dump()
# - added _get_episode/health_issue_names()
# - remove old workaround code
# - sort test output by age, oldest on top
#
# Revision 1.28  2003/06/27 16:03:50  ncq
# - no need for ; in DB-API queries
# - implement EMR text dump
#
# Revision 1.27  2003/06/26 21:24:49  ncq
# - cleanup re quoting + ";" and (cmd, arg) style
#
# Revision 1.26  2003/06/26 06:05:38  ncq
# - always add ; at end of sql queries but have space after %s
#
# Revision 1.25  2003/06/26 02:29:20  ihaywood
# Bugfix for searching for pre-existing health issue records
#
# Revision 1.24  2003/06/24 12:55:08  ncq
# - eventually make create_clinical_note() functional
#
# Revision 1.23  2003/06/23 22:28:22  ncq
# - finish encounter handling for now, somewhat tested
# - use gmPG.run_query changes where appropriate
# - insert_clin_note() finished but untested
# - cleanup
#
# Revision 1.22  2003/06/22 16:17:40  ncq
# - start dealing with encounter initialization
# - add create_clinical_note()
# - cleanup
#
# Revision 1.21  2003/06/19 15:22:57  ncq
# - fix spelling error in SQL in episode creation
#
# Revision 1.20  2003/06/03 14:05:05  ncq
# - start listening threads last in __init__ so we won't hang
#   if anything else fails in the constructor
#
# Revision 1.19  2003/06/03 13:17:32  ncq
# - finish default clinical episode/health issue handling, simple tests work
# - clinical encounter handling still insufficient
# - add some more comments to Syan's code
#
# Revision 1.18  2003/06/02 20:58:32  ncq
# - nearly finished with default episode/health issue stuff
#
# Revision 1.17  2003/06/01 16:25:51  ncq
# - preliminary code for episode handling
#
# Revision 1.16  2003/06/01 15:00:31  sjtan
#
# works with definite, maybe note definate.
#
# Revision 1.15  2003/06/01 14:45:31  sjtan
#
# definite and definate databases catered for, temporarily.
#
# Revision 1.14  2003/06/01 14:34:47  sjtan
#
# hopefully complies with temporary model; not using setData now ( but that did work).
# Please leave a working and tested substitute (i.e. select a patient , allergy list
# will change; check allergy panel allows update of allergy list), if still
# not satisfied. I need a working model-view connection ; trying to get at least
# a basically database updating version going .
#
# Revision 1.13  2003/06/01 14:15:48  ncq
# - more comments
#
# Revision 1.12  2003/06/01 14:11:52  ncq
# - added some comments
#
# Revision 1.11  2003/06/01 14:07:42  ncq
# - "select into" is an update command, too
#
# Revision 1.10  2003/06/01 13:53:55  ncq
# - typo fixes, cleanup, spelling definate -> definite
# - fix my obsolote handling of patient allergies tables
# - remove obsolete clin_transaction stuff
#
# Revision 1.9  2003/06/01 13:20:32  sjtan
#
# logging to data stream for debugging. Adding DEBUG tags when work out how to use vi
# with regular expression groups (maybe never).
#
# Revision 1.8  2003/06/01 12:55:58  sjtan
#
# sql commit may cause PortalClose, whilst connection.commit() doesnt?
#
# Revision 1.7  2003/06/01 01:47:32  sjtan
#
# starting allergy connections.
#
# Revision 1.6  2003/05/17 17:23:43  ncq
# - a little more testing in main()
#
# Revision 1.5  2003/05/05 00:06:32  ncq
# - make allergies work again after EMR rework
#
# Revision 1.4  2003/05/03 14:11:22  ncq
# - make allergy change signalling work properly
#
# Revision 1.3  2003/05/03 00:41:14  ncq
# - fetchall() returns list, not dict, so handle accordingly in "allergy names"
#
# Revision 1.2  2003/05/01 14:59:24  ncq
# - listen on allergy add/delete in backend, invalidate cache and notify frontend
# - "allergies", "allergy names" getters
#
# Revision 1.1  2003/04/29 12:33:20  ncq
# - first draft
#
