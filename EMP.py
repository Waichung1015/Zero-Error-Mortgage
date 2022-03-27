from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#connect to MySQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b65e280540657e:f1af7f27@us-cdbr-iron-east-03.cleardb.net/heroku_14b3224025d57d1'

#connect to MySQL from local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usrname:pwd@ip/database_schema'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/employer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init orm database
db = SQLAlchemy(app)

#tables

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
    employee_salary = db.Column(db.Numeric(12,2))
    done = db.Column(db.Boolean, default=False)

    def __init__(self, empname, emptitle, empdpt, employeename, employeeid, employeesalary):
        self.employer_name = empname
        self.employer_title = emptitle
        self.employer_dpt = empdpt
        self.employee_name = employeename
        self.employee_id = employeeid
        self.employee_salary = employeesalary

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
    mortgage_id = db.Column(db.Integer)
    form_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(45))

    def __init__(self, empid, mortid, company):
        self.emp_id = empid
        self.mortgage_id = mortid
        self.company = company

#GET - Employer Portal Home Page
@app.route('/', methods=['GET'])
def EmployerHomePage():
    return render_template('emp_main.html')

#GET/POST - Employer Portal Authentication Page
@app.route('/authentication', methods=['GET','POST'])
def Authentication():
    if request.method == 'GET':
        return render_template('authentication.html')
    else:
        empid = request.form['empID']
        empName = request.form['empName'].lower()
        result = employee_info.query.filter(employee_info.emp_id==empid).first()
        result2 = employer_form.query.filter(employer_form.employee_id==empid).first()
        done = "Not yet.."
        if result2 is not None:
            done = "Yes, you are ready to agree"      
        if result is not None and empName==result.emp_name.lower():
            row = employee_form.query.filter(employee_form.emp_id==empid).first()
            if row is None:
                return render_template('form.html', empid=empid)
            else:
                return render_template('FormInformation.html', empid=empid, row=row, done=done)
        #NEED A ERROR PAGE HERE

#GET/POST - Employee Form
@app.route('/form/<empid>', methods=['GET','POST'])
def EmployerPortalForm(empid):
    result = employee_form.query.filter(employee_form.emp_id==empid).first()
    result2 = employer_form.query.filter(employer_form.employee_id==empid).first()
    done = result2.done
    if request.method == 'GET':
        if result is not None:
            return render_template('FormInformation.html',empid=empid, row=result, done=done)
        else:
            return render_template('form.html', empid=empid)
    else:
        mortgageID = request.form['mortgageID']
        company = request.form['company']
        if result is None:
            create_input = employee_form(mortid=mortgageID, empid=empid, company=company)
            db.session.add(create_input)
            db.session.commit()
            return render_template('emp_main.html', rows=result, done=done)
        else:
            #EDIT

            result.mortgage_id = mortgageID
            result.company = company
            db.session.commit()
            return render_template('emp_main.html', rows=result, done=done)

#GET/POST Employer Form Submit Button
@app.route('/empForm/<empid>', methods=['GET','POST'])
def EmpForm(empid):
    result = employer_form.query.filter(employer_form.employee_id==empid).first()
    if request.method == 'GET':
        return render_template('empForm.html')
    else:
        if result is None:
            employerName = request.form['employerName']
            employerTitle = request.form['employerTitle']
            employerDepartment = request.form['employerDepartment']
            employeeName = request.form['employeeName']
            employeeID = request.form['employeeID']
            employeeID = int(employeeID)
            employeeSalary = float(request.form['empSalary'])
            create_input = employer_form(empname=employerName, emptitle=employerTitle,
                                 empdpt=employerDepartment, employeename=employeeName,
                                 employeeid=employeeID, employeesalary=employeeSalary)
            db.session.add(create_input)
            db.session.commit()
            result = employer_form.query.filter(employer_form.employee_id == employeeID).first()
            result.done = True
            db.session.commit()

            return render_template('emp_main.html')
        else:
            #EDIT
            result.employer_name = request.form['employerName']
            result.employer_title = request.form['employerTitle']
            result.emp_dpt = request.form['employerDepartment']
            result.employee_name = request.form['employeeName']
            result.employee_id = int(request.form['employeeID'])
            result.employee_salary = float(request.form['employeeSalary'])
            db.session.commit()
            return render_template('emp_main.html')

#GET/POST Employer Help Page
@app.route('/help', methods=['GET','POST'])
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
@app.route('/agree/<empid>', methods=['POST','GET'])
def Agree(empid):
    if request.method == 'GET':
        return render_template('Agree.html',empid=empid)

    # result1 = employer_form.query.filter(employer_form.employee_id==empid).first()
    # empname = result1.employee_name
    # result3 = employee_info.query.filter(employee_info.emp_id==empid).first()
    return redirect(url_for('EmployerHomePage'))

#get the Home Page for broker portal
# @app.route('/agree/<empid>', methods=['GET'])
# def ViewAgree(empid):
#     return render_template('Agree.html',empid=empid)

#get the Notification Page
# @app.route('/notification', methods=['GET'])
# def ViewNotification():
#     return render_template('Notification_MBR.html')

if __name__ == '__main__':
    app.run(debug=True)