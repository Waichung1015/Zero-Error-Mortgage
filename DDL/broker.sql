drop database if exists broker;
create database broker;
use broker;

create table if not exists broker_userinfo(
user_id int auto_increment primary key,
user_name varchar(45),
user_pwd varchar(45),
user_email varchar(45),
user_token varchar(225)
);

create table if not exists broker_mortgage_record(
user_id int,
mortgage_id int auto_increment primary key,
user_realname varchar(45),
user_company varchar(45),
user_phone varchar(45),
user_address varchar(45),
user_mortgage decimal,
employer_name varchar(45),
employer_title varchar(45),
employer_dpt varchar(45),
emp_id int,
user_salary int,
insurance_value int,
deductible_value int,
have_submitted bool,
have_emp_help bool,
is_insurable bool,
foreign key (user_id) references broker_userinfo(user_id)
);