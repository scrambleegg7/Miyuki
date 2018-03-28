use test

drop table if exists test5;

create table test5 (
	field1			varchar(40),
	primary key (field1)
)

ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;
