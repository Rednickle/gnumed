# -*- coding: latin-1 -*-
"""GNUmed provider inbox middleware.

This should eventually end up in a class cPractice.
"""
#============================================================
__license__ = "GPL"
__version__ = "$Revision: 1.14 $"
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"


import sys


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmPG2
from Gnumed.pycommon import gmBusinessDBObject
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDateTime

from Gnumed.business import gmStaff

#============================================================
# description
#------------------------------------------------------------
_SQL_get_inbox_messages = u"SELECT * FROM dem.v_message_inbox WHERE %s"

class cInboxMessage(gmBusinessDBObject.cBusinessDBObject):

	_cmd_fetch_payload = _SQL_get_inbox_messages % u"pk_inbox_message = %s"
	_cmds_store_payload = [
		u"""
			UPDATE dem.message_inbox SET
				fk_staff = %(pk_staff)s,
				fk_inbox_item_type = %(pk_type)s,
				comment = gm.nullify_empty_string(%(comment)s),
				data = gm.nullify_empty_string(%(data)s),
				importance = %(importance)s,
				fk_patient = %(pk_patient)s,
				ufk_context = %(pk_context)s,
				due_date = %(due_date)s,
				expiry_date = %(expiry_date)s
			WHERE
				pk = %(pk_inbox_message)s
					AND
				xmin = %(xmin_message_inbox)s
			RETURNING
				pk as pk_inbox_message,
				xmin as xmin_message_inbox
		"""
	]
	_updatable_fields = [
		u'pk_staff',
		u'pk_type',
		u'comment',
		u'data',
		u'importance',
		u'pk_patient',
		u'ufk_context',
		u'due_date',
		u'expiry_date'
	]
	#------------------------------------------------------------
	def format(self):
		tt = u'%s: %s%s\n' % (
			gmDateTime.pydt_strftime (
				self._payload[self._idx['received_when']],
				format = '%A, %Y %B %d, %H:%M',
				accuracy = gmDateTime.acc_minutes
			),
			gmTools.bool2subst(self._payload[self._idx['is_virtual']], _('virtual message'), _('message')),
			gmTools.coalesce(self._payload[self._idx['pk_inbox_message']], u'', u' #%s ')
		)

		tt += u'%s: %s\n' % (
			self._payload[self._idx['l10n_category']],
			self._payload[self._idx['l10n_type']]
		)

		tt += u'%s %s %s\n' % (
			self._payload[self._idx['modified_by']],
			gmTools.u_right_arrow,
			gmTools.coalesce(self._payload[self._idx['provider']], _('everyone'))
		)

		tt += u'\n%s%s%s\n\n' % (
			gmTools.u_left_double_angle_quote,
			self._payload[self._idx['comment']],
			gmTools.u_right_double_angle_quote
		)

		tt += gmTools.coalesce (
			self._payload[self._idx['pk_patient']],
			u'',
			u'%s\n\n' % _('Patient #%s')
		)

		tt += gmTools.coalesce (
			self._payload[self._idx['due_date']],
			u'',
			_('Due: %s\n'),
			function_initial = ('strftime', '%Y-%m-%d')
		)

		tt += gmTools.coalesce (
			self._payload[self._idx['expiry_date']],
			u'',
			_('Expiry: %s\n'),
			function_initial = ('strftime', '%Y-%m-%d')
		)

		if self._payload[self._idx['data']] is not None:
			tt += self._payload[self._idx['data']][:150]
			if len(self._payload[self._idx['data']]) > 150:
				tt += gmTools.u_ellipsis

		return tt
#------------------------------------------------------------
def get_due_messages(pk_patient=None, order_by=None):

	if order_by is None:
		order_by = u'%s ORDER BY due_date, importance DESC, received_when DESC'
	else:
		order_by = u'%%s ORDER BY %s' % order_by

	args = {'pat': pk_patient}
	where_parts = [
		u'pk_patient = %(pat)s',
		u'is_due IS TRUE'
	]

	cmd = u"SELECT *, now() - due_date AS interval_due FROM dem.v_message_inbox WHERE %s" % (
		order_by % u' AND '.join(where_parts)
	)
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)

	return [ cInboxMessage(row = {'data': r, 'idx': idx, 'pk_field': 'pk_inbox_message'}) for r in rows ]

#------------------------------------------------------------
def get_inbox_messages(pk_staff=None, pk_patient=None, include_without_provider=False, order_by=None):

	if order_by is None:
		order_by = u'%s ORDER BY importance desc, received_when desc'
	else:
		order_by = u'%%s ORDER BY %s' % order_by

	args = {}
	where_parts = []

	if pk_staff is not None:
		if include_without_provider:
			where_parts.append(u'pk_staff IN (%(staff)s, NULL) OR modified_by = (SELECT short_alias FROM dem.staff WHERE pk = %(staff)s)')
		else:
			where_parts.append(u'pk_staff = %(staff)s OR modified_by = (SELECT short_alias FROM dem.staff WHERE pk = %(staff)s)')
		args['staff'] = pk_staff

	if pk_patient is not None:
		where_parts.append(u'pk_patient = %(pat)s')
		args['pat'] = pk_patient

	cmd = _SQL_get_inbox_messages % (
		order_by % u' AND '.join(where_parts)
	)
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = True)

	return [ cInboxMessage(row = {'data': r, 'idx': idx, 'pk_field': 'pk_inbox_message'}) for r in rows ]
#------------------------------------------------------------
def create_inbox_message(message_type=None, subject=None, patient=None, staff=None):

	success, pk_type = gmTools.input2int(initial = message_type)
	if not success:
		pk_type = create_inbox_item_type(message_type = message_type)

	cmd = u"""
		INSERT INTO dem.message_inbox (
			fk_staff,
			fk_patient,
			fk_inbox_item_type,
			comment
		) VALUES (
			%(staff)s,
			%(pat)s,
			%(type)s,
			gm.nullify_empty_string(%(subject)s)
		)
		RETURNING pk
	"""
	args = {
		u'staff': staff,
		u'pat': patient,
		u'type': pk_type,
		u'subject': subject
	}
	rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], return_data = True, get_col_idx = False)

	return cInboxMessage(aPK_obj = rows[0]['pk'])
#------------------------------------------------------------
def delete_inbox_message(inbox_message=None):
	args = {'pk': inbox_message}
	cmd = u"DELETE FROM dem.message_inbox WHERE pk = %(pk)s"
	gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])
	return True
#------------------------------------------------------------
def create_inbox_item_type(message_type=None, category=u'clinical'):

	# determine category PK
	success, pk_cat = gmTools.input2int(initial = category)
	if not success:
		args = {u'cat': category}
		cmd = u"""SELECT COALESCE (
			(SELECT pk FROM dem.inbox_item_category WHERE _(description) = %(cat)s),
			(SELECT pk FROM dem.inbox_item_category WHERE description = %(cat)s)
		) AS pk"""
		rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}])
		if rows[0]['pk'] is None:
			cmd = u"INSERT INTO dem.inbox_item_category (description) VALUES (%(cat)s) RETURNING pk"
			rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], return_data = True)
			pk_cat = rows[0]['pk']
		else:
			pk_cat = rows[0]['pk']

	# find type PK or create type
	args = {u'cat': pk_cat, u'type': message_type}
	cmd = u"""SELECT COALESCE (
		(SELECT pk FROM dem.inbox_item_type where fk_inbox_item_category = %(cat)s and _(description) = %(type)s),
		(SELECT pk FROM dem.inbox_item_type where fk_inbox_item_category = %(cat)s and description = %(type)s)
	) AS pk"""
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}])
	if rows[0]['pk'] is None:
		cmd = u"""
			INSERT INTO dem.inbox_item_type (
				fk_inbox_item_category,
				description,
				is_user
			) VALUES (
				%(cat)s,
				%(type)s,
				TRUE
			) RETURNING pk"""
		rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], return_data = True)

	return rows[0]['pk']
#============================================================
#============================================================
class cProviderInbox:
	def __init__(self, provider_id=None):
		if provider_id is None:
			self.__provider_id = gmStaff.gmCurrentProvider()['pk_staff']
		else:
			self.__provider_id = provider_id
	#--------------------------------------------------------
	def delete_message(self, pk=None):
		return delete_inbox_message(inbox_message = pk)
	#--------------------------------------------------------
	def add_message(message_type=None, subject=None, patient=None):
		return create_inbox_message (
			message_type = message_type,
			subject = subject,
			patient = patient,
			staff = self.__provider_id
		)
	#--------------------------------------------------------
	# properties
	#--------------------------------------------------------
	def _get_messages(self):
		return get_inbox_messages(pk_staff = self.__provider_id)

	def _set_messages(self, messages):
		return

	messages = property(_get_messages, _set_messages)
#============================================================
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

	from Gnumed.pycommon import gmI18N

	gmI18N.activate_locale()
	gmI18N.install_domain()

	#---------------------------------------
	def test_inbox():
		gmStaff.gmCurrentProvider(provider = gmStaff.cStaff())
		inbox = cProviderInbox()
		for msg in inbox.messages:
			print msg
	#---------------------------------------
	def test_msg():
		msg = cInboxMessage(aPK_obj = 1)
		print msg
	#---------------------------------------
	def test_create_type():
		print create_inbox_item_type(message_type = 'test')
	#---------------------------------------
	def test_due():
		for msg in get_due_messages(pk_patient = 12):
			print msg.format()
	#---------------------------------------
	#test_inbox()
	#test_msg()
	#test_create_type()
	test_due()

#============================================================
