drop database if exists insurance;
create database insurance;
use insurance;

create table if not exists Insurance_application(
ID int auto_increment primary key,
`name` varchar(45),
re_address varchar(45),
re_value int(45),
work_company varchar(45),
work_depart varchar(45),
work_salary decimal,
has_reviewed bool,
reviewed_by varchar(45),
reviewed_result varchar(45)
);

create table if not exists Insurance_info(
ID int primary key,
insurance_value decimal,
deductible_value decimal,
property_address varchar(45),
property_manager varchar(45),
`name` varchar(45),
property_value int,
re_id int,
is_insurable bool,
foreign key(ID) references Insurance_application(ID)
);