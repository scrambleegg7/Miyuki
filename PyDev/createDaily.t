use test

drop table if exists daily;

create table daily (
	id int auto_increment not null,
	cdate			date,
	a_no			int,
	custNo			int,
	fullName		varchar(40) collate utf8_unicode_ci NOT NULL,
	healthIns 		varchar(40) not null,
	institution		varchar(40) not null,
	primary key (id,cdate,a_no,custNo,fullName)
)

ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;
