-- Project: GnuMed
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmClinicalData.sql,v $
-- $Id: gmClinicalData.sql,v 1.7 2003-05-04 23:59:35 ncq Exp $
-- license: GPL
-- author: Ian Haywood, Horst Herb

-- ===================================================================
-- This database is internationalised!

-- do fixed string i18n()ing
\i gmI18N.sql

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- ===================================================================
--		self.__consultation_types = [
--			_('in surgery'),
--			_('home visit'),
--			_('by phone'),
--			_('at specialist'),
--			_('patient absent'),
--			_('by email'),
--			_('other consultation')
--		]
INSERT INTO _enum_encounter_type (description) values (i18n('in surgery'));
INSERT INTO _enum_encounter_type (description) values (i18n('phone consultation'));
INSERT INTO _enum_encounter_type (description) values (i18n('fax consultation'));
INSERT INTO _enum_encounter_type (description) values (i18n('home visit'));
INSERT INTO _enum_encounter_type (description) values (i18n('nursing home visit'));
INSERT INTO _enum_encounter_type (description) values (i18n('repeat script'));
INSERT INTO _enum_encounter_type (description) values (i18n('hospital visit'));
INSERT INTO _enum_encounter_type (description) values (i18n('video conference'));
INSERT INTO _enum_encounter_type (description) values (i18n('proxy encounter'));
INSERT INTO _enum_encounter_type (description) values (i18n('emergency encounter'));
INSERT INTO _enum_encounter_type (description) values (i18n('other encounter'));

-- ===================================================================
insert into _enum_allergy_type (value) values (i18n('allergy'));
insert into _enum_allergy_type (value) values (i18n('sensitivity'));

-- ===================================================================
INSERT INTO _enum_hx_type (description) values (i18n('past'));
INSERT INTO _enum_hx_type (description) values (i18n('presenting complaint'));
INSERT INTO _enum_hx_type (description) values (i18n('history of present illness'));
INSERT INTO _enum_hx_type (description) values (i18n('social'));
INSERT INTO _enum_hx_type (description) values (i18n('family'));
INSERT INTO _enum_hx_type (description) values (i18n('immunisation'));
INSERT INTO _enum_hx_type (description) values (i18n('requests'));
INSERT INTO _enum_hx_type (description) values (i18n('allergies'));
INSERT INTO _enum_hx_type (description) values (i18n('drug'));
INSERT INTO _enum_hx_type (description) values (i18n('sexual'));
INSERT INTO _enum_hx_type (description) values (i18n('psychiatric'));
INSERT INTO _enum_hx_type (description) values (i18n('other'));

-- ===================================================================
insert into _enum_hx_source (description) values (i18n('patient'));
insert into _enum_hx_source (description) values (i18n('clinician'));
insert into _enum_hx_source (description) values (i18n('relative'));
insert into _enum_hx_source (description) values (i18n('carer'));
insert into _enum_hx_source (description) values (i18n('notes'));
insert into _enum_hx_source (description) values (i18n('correspondence'));

-- ===================================================================
INSERT INTO enum_coding_systems (description) values (i18n('general'));
INSERT INTO enum_coding_systems (description) values (i18n('clinical'));
INSERT INTO enum_coding_systems (description) values (i18n('diagnosis'));
INSERT INTO enum_coding_systems (description) values (i18n('therapy'));
INSERT INTO enum_coding_systems (description) values (i18n('pathology'));
INSERT INTO enum_coding_systems (description) values (i18n('bureaucratic'));
INSERT INTO enum_coding_systems (description) values (i18n('ean'));
INSERT INTO enum_coding_systems (description) values (i18n('other'));

-- ===================================================================
INSERT INTO enum_confidentiality_level (description) values (i18n('public'));
INSERT INTO enum_confidentiality_level (description) values (i18n('relatives'));
INSERT INTO enum_confidentiality_level (description) values (i18n('receptionist'));
INSERT INTO enum_confidentiality_level (description) values (i18n('clinical staff'));
INSERT INTO enum_confidentiality_level (description) values (i18n('doctors'));
INSERT INTO enum_confidentiality_level (description) values (i18n('doctors of practice only'));
INSERT INTO enum_confidentiality_level (description) values (i18n('treating doctor'));

-- ===================================================================
insert into drug_units(unit) values('ml');
insert into drug_units(unit) values('mg');
insert into drug_units(unit) values('mg/ml');
insert into drug_units(unit) values('mg/g');
insert into drug_units(unit) values('U');
insert into drug_units(unit) values('IU');
insert into drug_units(unit) values('each');
insert into drug_units(unit) values('mcg');
insert into drug_units(unit) values('mcg/ml');
insert into drug_units(unit) values('IU/ml');
insert into drug_units(unit) values('day');

-- ===================================================================
--I18N!
insert into drug_formulations(description) values ('tablet');
insert into drug_formulations(description) values ('capsule');
insert into drug_formulations(description) values ('syrup');
insert into drug_formulations(description) values ('suspension');
insert into drug_formulations(description) values ('powder');
insert into drug_formulations(description) values ('cream');
insert into drug_formulations(description) values ('ointment');
insert into drug_formulations(description) values ('lotion');
insert into drug_formulations(description) values ('suppository');
insert into drug_formulations(description) values ('solution');
insert into drug_formulations(description) values ('dermal patch');
insert into drug_formulations(description) values ('kit');

-- ===================================================================
--I18N!
insert into drug_routes(description, abbreviation) values('oral', 'o.');
insert into drug_routes(description, abbreviation) values('sublingual', 's.l.');
insert into drug_routes(description, abbreviation) values('nasal', 'nas.');
insert into drug_routes(description, abbreviation) values('topical', 'top.');
insert into drug_routes(description, abbreviation) values('rectal', 'rect.');
insert into drug_routes(description, abbreviation) values('intravenous', 'i.v.');
insert into drug_routes(description, abbreviation) values('intramuscular', 'i.m.');
insert into drug_routes(description, abbreviation) values('subcutaneous', 's.c.');
insert into drug_routes(description, abbreviation) values('intraarterial', 'art.');
insert into drug_routes(description, abbreviation) values('intrathecal', 'i.th.');

-- ===================================================================
insert into databases (name, published) values ('MIMS', '1/1/02');
insert into databases (name, published) values ('AMIS', '1/1/02');
insert into databases (name, published) values ('AMH', '1/1/02');

-- ===================================================================
insert into enum_immunities (name) values ('tetanus');

-- ===================================================================
-- do simple schema revision tracking
\i gmSchemaRevision.sql
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmClinicalData.sql,v $', '$Revision: 1.7 $');

-- =============================================
-- $Log: gmClinicalData.sql,v $
-- Revision 1.7  2003-05-04 23:59:35  ncq
-- - add comment on encounter types
--
-- Revision 1.6  2003/04/28 20:56:16  ncq
-- - unclash "allergy" in hx type and type of allergic reaction + translations
-- - some useful indices
--
-- Revision 1.5  2003/04/25 13:05:49  ncq
-- - adapt to frontend hookup for encounter types
--
-- Revision 1.4  2003/04/12 15:43:17  ncq
-- - adapted to new gmclinical.sql
--
-- Revision 1.3  2003/04/09 13:50:29  ncq
-- - typos
--
-- Revision 1.2  2003/04/09 13:08:21  ncq
-- - _clinical_ -> _clin_
--
-- Revision 1.1  2003/02/14 10:54:19  ncq
-- - breaking out enumerated data
--
