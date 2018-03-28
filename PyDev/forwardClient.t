use receipty

drop table if exists forwardClient;

create table forwardClient (
	id int auto_increment not null,
	nextIssueDate		date,
	clientName		varchar(40) collate utf8_unicode_ci NOT NULL,
	totalAmount			float,
	drugName varchar(80) collate utf8_unicode_ci,
	stockAmount			float,
        mu			float,
		std			float,
        msg1                    varchar(20),
        msg2                    varchar(20),
		
	primary key (id,nextissueDate,clientName,drugName)
)

ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;
