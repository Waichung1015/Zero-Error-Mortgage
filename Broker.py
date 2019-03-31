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
    insurance_value = db.Column(db.Integer)
    deductible_value = db.Column(db.Integer)
    MIsID = db.Column(db.Integer)
    ID = db.Column(db.Integer)
    have_submitted = db.Column(db.Boolean, default=False)
    have_emp_help = db.Column(db.Boolean, default=False)
    is_insurable = db.Column(db.Boolean, default=False)


    def __init__(self, userid, user_name, usercompany, userphone,
                 useradd, usermort, emp_name, emptitle, emp_dpt, usersalary, empid, insurable,
                 insurance, deductible,MIsID,ID):
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
        self.MIsID = MIsID
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
    MIsID = db.Column(db.Integer, primary_key=True)
    property_value = db.Column(db.Integer)
    def __init__(self, property):
        self.property_value = property


class RE_login(db.Model):
    __tablename__ = 'RE_login'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(45))
    user_pwd = db.Column(db.String(45))
    user_email = db.Column(db.String(45))

    def __init__(self, uname, pwd, email):
        self.user_name = uname
        self.user_pwd = pwd
        self.user_email = email


class RE_form(db.Model):
    __tablename__ = 'RE_form'
    form_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('RE_login.user_id'))
    name = db.Column(db.String(45))
    mortgage_id = db.Column(db.Integer)
    MIsID = db.Column(db.Integer, db.ForeignKey('RE_info.MIsID'))
    def __init__(self, userid, name, mortgage_id,MIsID):
        self.user_id = userid
        self.name = name
        self.mortgage_id = mortgage_id
        self.MIsID = MIsID

class Insurance_info(db.Model):
    __tablename__ = 'Insurance_info'
    insurance_value = db.Column(db.Integer)
    deductible_value = db.Column(db.Integer)
    name = db.Column(db.String(45))
    ID = db.Column(db.Integer, primary_key=True)
    property_value = db.Column(db.Integer,db.ForeignKey('RE_info.property_value'))
    is_insurable = db.Column(db.Boolean, default=False)
    def __init__(self, insurance, deductible, name, property, insurable):
        self.insurance_value = insurance
        self.deductible_value = deductible
        self.name = name
        self.property_value = property
        self.is_insurable = insurable

#get the Home Page for broker portal
@app.route('/broker_main.html', methods=['GET'])
def broker_home():
    return render_template('broker_main.html')

#GET brokerUserMenu Page
@app.route('/broker_userMenu.html/<userid>', methods=['GET','POST'])
def broker_userMenu(userid):
    if request.method == 'GET':
        username = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first().user_name
        return render_template('broker_userMenu.html', userid=userid, username=username)
    else:
        username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
        return render_template('broker_userMenu.html', userid=userid, username=username)

#POST - brokerUserMenu Page
#compare pwd - login
@app.route('/broker_main.html', methods=['POST'])
def broker_login():
    email = request.form['email']
    user_pwd = request.form['password']
    result = broker_userinfo.query.filter(broker_userinfo.user_email==email).first()
    user_id = result.user_id
    user_name = result.user_name
    if user_pwd == result.user_pwd:
        return render_template('broker_userMenu.html', userid=user_id, username=user_name)

#POST/GET - Submit Mortgage Application Form
#See all information
#Store information into table
@app.route('/application.html/<userid>', methods=['GET','POST'])
def ApplicationInformation(userid):
    result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id==userid).first()
    if request.method == 'GET':
        if result is None:
            return render_template('application.html', userid=userid)
        else:
            return render_template('ApplicationInformation.html', userid=userid, row=result)
    else:
        userRealName = request.form['userRealName']
        userCompany = request.form['userCompany']
        empid = request.form['empID']
        empid = int(empid)
        userPhoneNum = request.form['userPhoneNum']
        userAddress = request.form['userAddress']
        userMortgage = request.form['userMortgage']
        MIsID = request.form['MIsID']
        userMortgage = float(userMortgage)
        MIsID = int(MIsID)
        create_input = broker_mortgage_record(userid=userid, user_name=userRealName, usercompany=userCompany,
                                              userphone=userPhoneNum, useradd=userAddress, usermort=userMortgage, MIsID=MIsID, empid=empid,
                                              emp_name="None", emptitle="None", emp_dpt="None", usersalary=0, insurable=False,
                                              insurance=0, deductible=0, ID=0)
        if result is not None:
            result.user_realname = request.form['userRealName']
            result.user_company = request.form['userCompany']
            result.user_phone = request.form['userPhoneNum']
            result.user_address = request.form['userAddress']
            result.user_mortgage = request.form['userMortgage']
            result.emp_id = request.form['empID']
            result.MIsID = request.form['MIsID']
            db.session.commit()
            username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
            return render_template('broker_userMenu.html', userid=userid, username=username)
        else:
            db.session.add(create_input)
            db.session.commit()
            result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
            result.have_submitted = True
            db.session.commit()
            mortgageid = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first().mortgage_id
            return render_template('Confirmation.html', userid=userid, mortgageid=mortgageid)

@app.route('/Confirmation/<userid>', methods=['GET'])
def Confirmation(userid):
    username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
    return render_template('broker_userMenu.html', userid=userid, username=username)


@app.route('/broker_main.html/<userid>', methods=['GET'])
def GoBack(userid):
    username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
    return render_template('broker_userMenu.html', userid=userid, username=username)

#GET - Mortgage Application Status
@app.route('/user_status.html/<userid>', methods=['GET'])
def broker_MortgageStatus(userid):
    result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
    result2 = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first()
    username = result2.user_name
    return render_template('user_status.html',userid=userid, rows=result, username=username)

#GET - Insurance Details
@app.route('/insurance_detail.html/<userid>', methods=['GET'])
def Insurance_Detail(userid):
    result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
    result2 = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first()
    username = result2.user_name
    return render_template('insurance_detail.html',userid=userid, rows=result, username=username)

#GET/POST SignUp Page
@app.route('/broker_signUp.html', methods=['GET','POST'])
def SignUp():
    if request.method == 'GET':
        return render_template('broker_signUp.html')
    else:
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        create_input = broker_userinfo(name=username, pwd=pwd, email=email)
        db.session.add(create_input)
        db.session.commit()

        return render_template('broker_main.html')


if __name__ == '__main__':
    app.run(debug=True)