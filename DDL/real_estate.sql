drop database if exists real_estate;
create database real_estate;
use real_estate;

create table if not exists RE_info(
MIsID int auto_increment primary key,
property_value int,
property_years int,
management_fee decimal,
purchased_time varchar(45),
manager varchar(45),
property_address varchar(45)
);

create table if not exists RE_login(
user_id int auto_increment primary key,
user_name varchar(45),
user_pwd varchar(45),
user_email varchar(45)
);

create table if not exists RE_form(
form_id int auto_increment primary key,
user_email varchar(45),
`name` varchar(45),
phone varchar(45),
property_address varchar(45)
);

insert into RE_info (property_value,
property_years,
management_fee,
purchased_time,
manager, property_address) values(300000, 50, 1000, "2010-03-20", "Johnathon, Private", "1010 queen st");
insert into RE_info (property_value,
property_years,
management_fee,
purchased_time,
manager, property_address) values(344430, 100, 1500, "2018-05-22", "re_company", "1221 prince rd");
insert into RE_info (property_value,
property_years,
management_fee,
purchased_time,
manager, property_address) values(422345, 100, 1500, "2008-07-14", "re_company", "3101 spring garden rd");
insert into RE_info (property_value,
property_years,
management_fee,
purchased_time,
manager, property_address) values(125233, 100, 1500, "2019-09-10", "re_company", "1055 university ave");