-- =============================================
-- GnuMed fixed string internationalisation
-- ========================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmI18N.sql,v $
-- $Id: gmI18N.sql,v 1.6 2003-01-20 20:21:53 ncq Exp $
-- license: GPL
-- author: Karsten.Hilbert@gmx.net
-- =============================================
-- Include this file at the top of your psql script schema definition files.
-- For your convenience, just copy/paste the following two lines:
-- do fixed string i18n()ing
--\i gmI18N.sql

-- This will allow for transparent translation of 'fixed'
-- strings in the database. Simply switching the language in
-- i18n_curr_lang will enable the user to see another language.

-- For details please see the Developer's Guide.
-- =============================================
\unset ON_ERROR_STOP

create table i18n_curr_lang (
	id serial primary key,
	owner varchar(20) default CURRENT_USER unique not null,
	lang varchar(10) not null
);

comment on table i18n_curr_lang is
	'holds the currently selected language per user for fixed strings in the database';

-- =============================================
create table i18n_keys (
	id serial primary key,
	orig text unique
);

comment on table i18n_keys is
	'this table holds all the original strings that need translation so give this to your language teams,
	the function _() will take care to enter relevant strings into this table,
	the table table does NOT play any role in runtime translation activity';

-- =============================================
create table i18n_translations (
	id serial primary key,
	lang varchar(10),
	orig text,
	trans text,
	unique (lang, orig)
);
create index idx_orig on i18n_translations(orig);

-- =============================================
drop function i18n(text);

create function i18n(text) returns text as '
DECLARE
	original ALIAS FOR $1;
BEGIN
	if not exists(select id from i18n_keys where orig = original) then
		insert into i18n_keys (orig) values (original);
	end if;
	return original;
END;
' language 'plpgsql';

comment on function i18n(text) is
	'insert original strings into i18n_keys for later translation';

-- =============================================
drop function _(text);

create function _(text) returns text as '
DECLARE
	orig_str ALIAS FOR $1;
	trans_str text;
	my_lang varchar(10);
BEGIN
	-- no translation available at all ?
	if not exists(select orig from i18n_translations where orig = orig_str) then
		return orig_str;
	end if;

	-- get language
	select into my_lang lang
		from i18n_curr_lang
	where
		owner = CURRENT_USER::varchar;
	if not found then
		return orig_str;
	end if;

	-- get translation
	select into trans_str trans
		from i18n_translations
	where
		lang = my_lang
			and
		orig = orig_str;
	if not found then
		return orig_str;
	end if;
	return trans_str;
END;
' language 'plpgsql';

comment on function _(text) is
	'will return either the input or the translation if it exists,
	 to be used as an after-select trigger function on your tables';

-- =============================================
--create function set_lang (text) returns unknown as '
--	delete from lang;
--	insert into lang (code) values ($1);
--	select NULL;
--' language 'sql';

\set ON_ERROR_STOP 1
-- =============================================
-- there's most likely no harm in granting select to all
GRANT SELECT on
	i18n_curr_lang,
	i18n_keys,
	i18n_translations
TO group "gm-public";

-- users need to be able to change this
-- FIXME: more groups need to have access here
GRANT SELECT, INSERT, UPDATE, DELETE on
	i18n_curr_lang
TO group "_gm-doctors";

-- =============================================
-- do simple schema revision tracking
\i gmSchemaRevision.sql
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmI18N.sql,v $', '$Revision: 1.6 $');

-- =============================================
-- $Log: gmI18N.sql,v $
-- Revision 1.6  2003-01-20 20:21:53  ncq
-- - keep the last useful bit from i18n.sql as documentation
--
-- Revision 1.5  2003/01/20 19:42:47  ncq
-- - simplified creation of translating view a lot
--
-- Revision 1.4  2003/01/17 00:24:33  ncq
-- - add a few access right definitions
--
-- Revision 1.3  2003/01/05 13:05:51  ncq
-- - schema_revision -> gm_schema_revision
--
-- Revision 1.2  2003/01/04 10:30:26  ncq
-- - better documentation
-- - insert default english "translation" into i18n_translations
--
-- Revision 1.1  2003/01/01 17:41:57  ncq
-- - improved database i18n
--
