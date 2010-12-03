-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1
set check_function_bodies to 'on';
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
select audit.add_table_for_audit('ref', 'consumable_substance');
select gm.add_table_for_notifies('ref', 'consumable_substance');



comment on table ref.consumable_substance is
'lists substances that are consumable by patients,
 whether or not linked to a branded drug';



-- .description
comment on column ref.consumable_substance.description is
	'The substance name.';

\unset ON_ERROR_STOP
alter table ref.consumable_substance drop constraint ref_subst_sane_desc cascade;
drop index ref.idx_subst_description cascade;
\set ON_ERROR_STOP 1

alter table ref.consumable_substance
	add constraint ref_subst_sane_desc
		check (gm.is_null_or_blank_string(description) is False);

create unique index idx_subst_description on ref.consumable_substance(description);



-- .atc_code
comment on column ref.consumable_substance.atc_code is
	'The Anatomic Therapeutic Chemical code for this substance.';

\unset ON_ERROR_STOP
alter table ref.consumable_substance drop constraint ref_subst_sane_atc cascade;
\set ON_ERROR_STOP 1

alter table ref.consumable_substance
	add constraint ref_subst_sane_atc
		check (gm.is_null_or_non_empty_string(atc_code) is True);



-- grants
grant select, insert, update, delete on
	ref.consumable_substance,
	ref.consumable_substance_pk_seq
to group "gm-doctors";



-- --------------------------------------------------------------
-- transfer old substances from ...

-- ... clin.consumed_substance
insert into ref.consumable_substance (
	description,
	atc_code
) select
	description,
	atc_code
from
	clin.consumed_substance ccs
where
	not exists (
		select 1
		from ref.consumable_substance rcs
		where rcs.description = ccs.description
	)
;

-- ... ref.substance_in_brand
insert into ref.consumable_substance (
	description,
	atc_code
) select
	rsib.description,
	rsib.atc_code
from
	ref.substance_in_brand rsib
where
	not exists (
		select 1
		from ref.consumable_substance rcs
		where rcs.description = rsib.description
	)
;

-- --------------------------------------------------------------
-- MUST protect from changing if in use directly or indirectly
\unset ON_ERROR_STOP
drop function ref.trf_do_not_update_substance_if_taken_by_patient() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_do_not_update_substance_if_taken_by_patient()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_msg text;
BEGIN
	if OLD.description = NEW.description then
		return NEW;
	end if;

	_msg := ''[ref.trf_do_not_update_substance_if_taken_by_patient]: as long as substance <%> is taken by a patient you cannot modify it'', OLD.description;

	perform 1 from clin.substance_intake c_si
	where c_si.fk_substance = OLD.pk
	limit 1;

	if FOUND then
		raise exception ''%'', _msg;
	end if;

	perform 1
	from clin.substance_intake c_si
	where c_si.fk_drug_component = (
		select r_ls2b.pk
		from ref.lnk_substance2brand r_ls2b
		where r_ls2b.fk_substance = OLD.pk
	)
	limit 1;

	if FOUND then
		raise exception ''%'', _msg;
	end if;

	return NEW;
END;';

comment on function ref.trf_do_not_update_substance_if_taken_by_patient() is
'If this substance is taken by any patient do not modify it (description).';

create trigger tr_do_not_update_substance_if_taken_by_patient
	before update
	on ref.consumable_substance
	for each row execute procedure ref.trf_do_not_update_substance_if_taken_by_patient()
;

-- --------------------------------------------------------------
-- sample data
\unset ON_ERROR_STOP
insert into ref.consumable_substance (
	description,
	atc_code
) values
	('Ibuprofen', 'M01AE01'),
	('tobacco', 'N07BA01'),
	('nicotine', 'N07BA01'),
	('alcohol', 'V03AB16'),
	('Tabak', 'N07BA01'),
	('Nikotin', 'N07BA01'),
	('Alkohol', 'V03AB16')
;
\set ON_ERROR_STOP 1



delete from ref.consumable_substance where description like '%-Starship';

insert into ref.consumable_substance (
	description,
	atc_code
) values (
	'Ibuprofen-Starship',
	'M01AE01'
);



delete from ref.branded_drug where description like '% Starship Enterprises';

insert into ref.branded_drug (
	description,
	preparation,
	atc_code,
	is_fake
) values (
	'IbuStrong Starship Enterprises',
	'tablet',
	'M01AE01',
	True
);

-- --------------------------------------------------------------
select gm.log_script_insertion('v12-ref-consumable_substance-dynamic.sql', 'Revision: 1.1');

-- ==============================================================
