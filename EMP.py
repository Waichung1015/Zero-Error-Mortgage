from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dockeruser:123456@134.190.159.227/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init orm database
db = SQLAlchemy(app)

#tables
"""
broker_userinfo is about information of broker users
"""
class broker_userinfo(db.Model):
    __tablename__ = "broker_userinfo"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(45))
    user_pwd = db.Column(db.String(45))
    user_email = db.Column(db.String(45))

    def __init__(self, name, pwd, email):
        self.user_name = name
        self.user_pwd = pwd
        self.user_email = email

"""
employer_form is for the employer to fill the form to help employee get mortgage
belongs to broker db
"""
class employer_form(db.Model):
    __tablename__ = 'employer_form'
    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employer_name = db.Column(db.String(45))
    employer_title = db.Column(db.String(45))
    employer_dpt = db.Column(db.String(45))
    employee_name = db.Column(db.String(45))
    employee_id = db.Column(db.Integer)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, empname, emptitle, empdpt, employeename, employeeid):
        self.employer_name = empname
        self.employer_title = emptitle
        self.employer_dpt = empdpt
        self.employee_name = employeename
        self.employee_id = employeeid

"""
broker_mortgage_record is to store info about mortgage record
belongs to broker
"""
class broker_mortgage_record(db.Model):
    __tablename__ = 'broker_mortgage_record'
    mortgage_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('broker_userinfo.user_id'))
    emp_id = db.Column(db.Integer)
    form_id = db.Column(db.Integer, db.ForeignKey('employer_form.form_id'))
    user_realname = db.Column(db.String(45))
    user_company = db.Column(db.String(45))
    user_phone = db.Column(db.String(45))
    user_address = db.Column(db.String(45))
    user_mortgage = db.Column(db.Numeric(12,2))
    employer_name = db.Column(db.String(45))
    employer_title = db.Column(db.String(45))
    employer_dpt = db.Column(db.String(45))
    user_salary = db.Column(db.Integer)
    ID = db.Column(db.Integer)
    insurance_value = db.Column(db.Integer)
    deductible_value = db.Column(db.Integer)
    have_submitted = db.Column(db.Boolean, default=False)
    have_emp_help = db.Column(db.Boolean, default=False)
    is_insurable = db.Column(db.Boolean, default=False)


    def __init__(self, userid, user_name, usercompany, userphone,
                 useradd, usermort, emp_name, emptitle, emp_dpt, usersalary, empid, insurable,
                 insurance, deductible, ID):
        self.user_id = userid
        self.user_realname = user_name
        self.user_company = usercompany
        self.user_phone = userphone
        self.user_address  =useradd
        self.user_mortgage = usermort
        self.employer_name = emp_name
        self.employer_title = emptitle
        self.employer_dpt = emp_dpt
        self.user_salary = usersalary
        self.emp_id = empid
        self.ID = ID
        self.is_insurable = insurable
        self.insurance_value = insurance
        self.deductible_value = deductible

"""
employee_info is to store info about employee to do authentication in employer's portal
belongs to employer portal
"""
class employee_info(db.Model):
    __tablename__ = 'employee_info'
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(45))
    emp_title = db.Column(db.String(45))
    emp_work_time = db.Column(db.Numeric(12,2))
    emp_salary = db.Column(db.Numeric(12,2))
    emp_dpt = db.Column(db.String(45))

    def __init__(self, empid, empname, emptitle, empworktime, empsalary, empDpt):
        self.emp_id = empid
        self.emp_name = empname
        self.emp_title = emptitle
        self.emp_work_time = empworktime
        self.emp_salary = empsalary
        self.emp_dpt = empDpt

class employee_form(db.Model):
    __tablename__ = 'employee_form'
    emp_id = db.Column(db.Integer, db.ForeignKey('employee_info.emp_id'))
    mortgage_id = db.Column(db.Integer, db.ForeignKey('broker_mortgage_record.mortgage_id'))
    form_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(45))

    def __init__(self, empid, mortid, address):
        self.emp_id = empid
        self.mortgage_id = mortid
        self.address = address

class RE_info(db.Model):
    __tablename__ = 'RE_info'
    RE_id = db.Column(db.Integer, primary_key=True)
    property_value = db.Column(db.Integer)
    mortgage_id = db.Column(db.Integer, db.ForeignKey('broker_mortgage_record.mortgage_id'))
    def __init__(self, re, property, mortgage):
        self.RE_id = re
        self.property_value = property
        self.mortgage_id = mortgage

class Insurance_info(db.Model):
    __tablename__ = 'Insurance_info'
    insurance_value = db.Column(db.Integer)
    deductible_value = db.Column(db.Integer)
    name = db.Column(db.String(45))
    MIsID = db.Column(db.Integer, primary_key=True)
    property_value = db.Column(db.Integer,db.ForeignKey('RE_info.property_value'))
    is_insurable = db.Column(db.Boolean, default=False)
    def __init__(self, insurance, deductible, name, MIsID, property, insurable):
        self.insurance_value = insurance
        self.deductible_value = deductible
        self.name = name
        self.MIsID = MIsID
        self.property_value = property
        self.is_insurable = insurable

#GET - Employer Portal Home Page
@app.route('/emp_main.html', methods=['GET'])
def EmployerHomePage():
    return render_template('emp_main.html')

#GET/POST - Employer Portal Authentication Page
@app.route('/authentication.html', methods=['GET','POST'])
def Authentication():
    if request.method == 'GET':
        return render_template('authentication.html')
    else:
        empid = request.form['empID']
        result = employee_info.query.filter(employee_info.emp_id==empid).first()
        if result is not None:
            row = employee_form.query.filter(employee_form.emp_id==empid).first()
            if row is None:
                return render_template('form.html', empid=empid)
            else:
                return render_template('FormInformation.html', empid=empid, row=row)
        #NEED A ERROR PAGE HERE

#GET/POST - Employee Form
@app.route('/form.html/<empid>', methods=['GET','POST'])
def EmployerPortalForm(empid):
    result = employee_form.query.filter(employee_form.emp_id==empid).first()
    if request.method == 'GET':
        if result is not None:
            return render_template('FormInformation.html',empid=empid, row=result)
        else:
            return render_template('form.html', empid=empid)
    else:
        mortgageID = request.form['mortgageID']
        url = request.form['url']
        if result is None:
            create_input = employee_form(mortid=mortgageID, empid=empid, address=url)
            db.session.add(create_input)
            db.session.commit()
            return render_template('emp_main.html', rows=result)
        else:
            #EDIT
            result.mortgage_id = mortgageID
            result.address = url
            db.session.commit()
            return render_template('emp_main.html', rows=result)

#GET/POST Employer Form Submit Button
@app.route('/empForm.html/<empid>', methods=['GET','POST'])
def EmpForm(empid):
    result = employer_form.query.filter(employer_form.employee_id==empid).first()
    if request.method == 'GET':
        return render_template('empForm.html')
    else:
        if result is None:
            print("error")
            employerName = request.form['employerName']
            employerTitle = request.form['employerTitle']
            employerDepartment = request.form['employerDepartment']
            employeeName = request.form['employeeName']
            employeeID = request.form['employeeID']
            employeeID = int(employeeID)
            create_input = employer_form(empname=employerName, emptitle=employerTitle,
                                 empdpt=employerDepartment, employeename=employeeName,
                                 employeeid=employeeID)
            db.session.add(create_input)
            db.session.commit()
            result = employer_form.query.filter(employer_form.employee_id == employeeID).first()
            result.done = True
            db.session.commit()

            return render_template('emp_main.html')
        else:
            #EDIT
            print(result.employee_id)
            result.employer_name = request.form['employerName']
            result.employer_title = request.form['employerTitle']
            result.emp_dpt = request.form['employerDepartment']
            result.employee_name = request.form['employeeName']
            result.employee_id = int(request.form['employeeID'])
            db.session.commit()
            return render_template('emp_main.html')

#GET/POST Employer Help Page
@app.route('/help.html', methods=['GET','POST'])
def Help():
    if request.method == 'GET':
        return render_template('help.html')
    else:
        name = request.form['empName']
        dpt = request.form['empDpt']
        result = employee_info.query.filter(employee_info.emp_name==name and employee_info.emp_dpt==dpt).first()
        if result is not None:
            empid = result.emp_id
            forminfo = employer_form.query.filter(employer_form.employee_id == empid).first()
            if forminfo is not None:
                return render_template('EmployerFormInformation.html', empid=empid, row=forminfo)
            else:
                return render_template('empForm.html', empid=empid)

#POST Agree Button
@app.route('/Agree.html/<empid>', methods=['POST'])
def Agree(empid):
    result1 = employer_form.query.filter(employer_form.employee_id==empid).first()
    empname = result1.employee_name
    result2 = broker_mortgage_record.query.filter(broker_mortgage_record.emp_id==empid and broker_mortgage_record.user_realname==empname).first()
    result3 = employee_info.query.filter(employee_info.emp_id==empid).first()

    result2.employer_name = result1.employer_name
    result2.employer_dpt = result1.employer_dpt
    result2.employer_title = result1.employer_title
    result2.user_salary = result3.emp_salary
    result2.have_emp_help = True
    result2.form_id = result1.form_id
    db.session.commit()
    return render_template('Notification_MBR.html')

#get the Home Page for broker portal
@app.route('/Agree.html<empid>', methods=['GET'])
def ViewAgree(empid):
    return render_template('Agree.html',empid=empid)

#get the Notification Page
@app.route('/Notification_MBR.html', methods=['GET'])
def ViewNotification():
    return render_template('Notification_MBR.html')

if __name__ == '__main__':
    app.run(debug=True)