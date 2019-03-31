drop database project;
create database project;
use project;

create table if not exists broker_userinfo(
user_id int auto_increment primary key,
user_name varchar(45),
user_pwd varchar(45),
user_email varchar(45)
);

create table if not exists employer_form(
form_id int auto_increment primary key,
employer_name varchar(45),
employer_title varchar(45),
employer_dpt varchar(45),
done bool,
employee_name varchar(45),
employee_id int
);

create table if not exists broker_mortgage_record(
user_id int,
mortgage_id int auto_increment primary key,
form_id int,
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
MIsID int,
ID int,
insurance_value int,
deductible_value int,
have_submitted bool,
have_emp_help bool,
is_insurable bool,
foreign key (user_id) references broker_userinfo(user_id),
foreign key (form_id) references employer_form(form_id)
);

create table if not exists employee_info(
emp_id int auto_increment primary key,
emp_name varchar(45),
emp_title varchar(45),
emp_work_time decimal,
emp_salary decimal,
emp_dpt varchar(45)
);

create table if not exists employee_form(
mortgage_id int,
emp_id int,
form_id int auto_increment primary key,
address varchar(45),
#foreign key (mortgage_id) references broker_mortgage_record(mortgage_id),
foreign key (emp_id) references employee_info(emp_id)
);

create table if not exists RE_info(
MIsID int auto_increment primary key,
property_value int
);

create table if not exists RE_login(
user_id int auto_increment primary key,
user_name varchar(45),
user_pwd varchar(45),
user_email varchar(45)
);

create table if not exists RE_form(
form_id int auto_increment primary key,
user_id int,
`name` varchar(45),
mortgage_id int,
MIsID int,
foreign key (user_id) references RE_login(user_id),
foreign key (MIsID) references RE_info(MIsID)
);

create table if not exists Insurance_info(
insurance_value int,
deductible_value int,
`name` varchar(45),
ID int auto_increment primary key,
property_value int,
re_id int,
is_insurable bool
);


insert into broker_userinfo (user_name, user_pwd, user_email) values ('name', 'pwd', 'name@email.com');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Florence', 'employee', 40, 5486, 'department-02');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Employer', 'employer', 40, 8000, 'department-01');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Sijia Zhou', 'employee', 40, 6666, 'department-03');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Ivy', 'employ', 40, 7777, 'department-04');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('BBB', 'employee', 40, 7777, 'department-04');

insert into RE_info (property_value) value(24435);
insert into RE_info (property_value) value(34443);
insert into RE_info (property_value) value(42234);
insert into RE_info (property_value) value(12523);

insert into RE_login(user_name, user_pwd, user_email) values ('name', 'pwd', 'name@mail.com');