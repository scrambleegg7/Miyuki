use test

drop table if exists test2;

create table test2 (
	id int auto_increment not null,
	field1			char(10),
	primary key (id,field1)
)

ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;
