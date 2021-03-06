-- Projekt GNUmed
-- test data for Enterprise Nurse Christine Chapel

-- author: Karsten Hilbert <Karsten.Hilbert@gmx.net>
-- license: GPL v2 or later
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/test-data/test_data-Christine_Chapel.sql,v $
-- $Revision: 1.12 $
-- =============================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- =============================================
insert into dem.identity (gender, dob, cob, title)
values ('f', '1932-2-23+2:00', 'US', 'Dr.RN');

insert into dem.names (id_identity, active, lastnames, firstnames)
values (currval('dem.identity_pk_seq'), true, 'Chapel', 'Christine');

insert into dem.staff (fk_identity, fk_role, db_user, short_alias, comment)
values (
	currval('dem.identity_pk_seq'),
	(select pk from dem.staff_role where name='nurse'),
	'test-nurse',
	'CC',
	'Enterprise Head Nurse, temporarily Enterprise Chief Medical Officer'
);

-- =============================================
-- do simple schema revision tracking
select log_script_insertion('$RCSfile: test_data-Christine_Chapel.sql,v $', '$Revision: 1.12 $');

-- =============================================
-- $Log: test_data-Christine_Chapel.sql,v $
-- Revision 1.12  2006-01-23 22:10:57  ncq
-- - staff.sign -> .short_alias
--
-- Revision 1.11  2006/01/06 10:12:03  ncq
-- - add missing grants
-- - add_table_for_audit() now in "audit" schema
-- - demographics now in "dem" schema
-- - add view v_inds4vaccine
-- - move staff_role from clinical into demographics
-- - put add_coded_term() into "clin" schema
-- - put German things into "de_de" schema
--
-- Revision 1.10  2005/11/25 15:07:28  ncq
-- - create schema "clin" and move all things clinical into it
--
-- Revision 1.9  2005/09/19 16:38:52  ncq
-- - adjust to removed is_core from gm_schema_revision
--
-- Revision 1.8  2005/07/14 21:31:43  ncq
-- - partially use improved schema revision tracking
--
-- Revision 1.7  2005/02/12 13:49:14  ncq
-- - identity.id -> identity.pk
-- - allow NULL for identity.fk_marital_status
-- - subsequent schema changes
--
-- Revision 1.6  2004/06/02 13:46:46  ncq
-- - setting default session timezone has incompatible syntax
--   across version range 7.1-7.4, henceforth specify timezone
--   directly in timestamp values, which works
--
-- Revision 1.5  2004/06/02 00:14:46  ncq
-- - add time zone setting
--
-- Revision 1.4  2004/01/18 21:59:06  ncq
-- - no clinical data hence no mention in xln_identity
--
-- Revision 1.3  2004/01/14 10:42:05  ncq
-- - use xlnk_identity
--
-- Revision 1.2  2004/01/10 02:00:44  ncq
-- - first names <-> last names
--
-- Revision 1.1  2004/01/10 01:29:25  ncq
-- - add test data for test-nurse, test-doctor
--
