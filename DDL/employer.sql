drop database if exists employer;
create database employer;
use employer;

create table if not exists employer_form(
form_id int auto_increment primary key,
employer_name varchar(45),
employer_title varchar(45),
employer_dpt varchar(45),
done bool,
employee_name varchar(45),
employee_id int,
employee_salary decimal
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
company varchar(45),
foreign key (emp_id) references employee_info(emp_id)
);

insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Florence', 'employee', 40, 5486, 'department-02');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Employer', 'employer', 40, 8000, 'department-01');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Employee', 'employee', 40, 6666, 'department-03');
insert into employee_info (emp_name, emp_title, emp_work_time, emp_salary, emp_dpt) values ('Ivy', 'employ', 40, 7777, 'department-04');