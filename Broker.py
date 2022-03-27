from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from flask_mail import Mail, Message
import oauth as oa, json
from Config import app

#mail = Mail(app)

#connect to MySQL from Heroku
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b65e280540657e:f1af7f27@us-cdbr-iron-east-03.cleardb.net/heroku_14b3224025d57d1'

#connect to MySQL from Local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usrname:pwd@ip/database_schema'

#init orm database
db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'index'

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
    user_token = db.Column(db.String(225))

    def __init__(self, name, pwd, email,token):
        self.user_name = name
        self.user_pwd = pwd
        self.user_email = email
        self.user_token = token


"""
broker_mortgage_record is to store info about mortgage record
belongs to broker
"""
class broker_mortgage_record(db.Model):
    __tablename__ = 'broker_mortgage_record'
    mortgage_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('broker_userinfo.user_id'))
    emp_id = db.Column(db.Integer)
    user_realname = db.Column(db.String(45))
    user_company = db.Column(db.String(45))
    user_phone = db.Column(db.String(45))
    user_address = db.Column(db.String(45))
    user_mortgage = db.Column(db.Numeric(12,2))
    employer_name = db.Column(db.String(45))
    employer_title = db.Column(db.String(45))
    employer_dpt = db.Column(db.String(45))
    user_salary = db.Column(db.Integer)
    re_address = db.Column(db.String(64))
    insurance_value = db.Column(db.Integer)
    deductible_value = db.Column(db.Integer)
    insurance_company = db.Column(db.String(64))
    have_submitted = db.Column(db.Boolean, default=False)
    have_emp_help = db.Column(db.Boolean, default=False)
    is_insurable = db.Column(db.Boolean, default=False)


    def __init__(self, userid, user_name, usercompany, userphone,
                 useradd, usermort, emp_name, emptitle, emp_dpt, usersalary, empid, insurable,
                 insurance, deductible, address, ins_company):
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
        self.is_insurable = insurable
        self.insurance_value = insurance
        self.deductible_value = deductible
        self.re_address = address
        self.insurance_company = ins_company

"""
OAuth User db
"""
class User(UserMixin, db.Model):
    """docstring for User"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@app.route('/error', methods=['GET'])
def error():
    return render_template('Error.html')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

#OAuth Login
@app.route('/authorize/<provider>')
def oauth_login(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('oauth_callback',provider=provider))
    oauth = oa.OAuthSignIn.get_provider(provider)
    return oauth.authorize()

#OAuth complete Login, call back to application
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        email = current_user.email
        userid = broker_userinfo.query.filter(broker_userinfo.user_email==email).first().user_id
        return redirect(url_for('broker_userMenu', userid=userid))
    oauth = oa.OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:  # social id is invalid
        flash('Authentication failed')
        return redirect(url_for('error'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
        account = broker_userinfo(name=username, pwd="", email=email, token=None)
        db.session.add(account)
        db.session.commit()
    userid = broker_userinfo.query.filter(broker_userinfo.user_email==email).first().user_id
    login_user(user, True)
    return redirect(url_for('broker_userMenu', userid=userid))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_home'))

@app.route('/', methods=['GET', 'POST'])
def get_home():
    if request.method == 'GET':
        return render_template('broker_main.html')
    else:
        email = request.form['email']
        user_pwd = request.form['password']
        result = broker_userinfo.query.filter(broker_userinfo.user_email==email).first()
        if result is None:
            return redirect(url_for('error'))
        user_id = result.user_id
        user_name = result.user_name
        if user_pwd == result.user_pwd:
            return redirect(url_for('broker_userMenu', userid=user_id))
    

#GET: the Home Page for broker portal
#POST: Login
# @app.route('/brokerhome', methods=['GET','POST'])
# def broker_home():
#     if request.method == 'GET':
#         return redirect('get_home')
#     else:
#         email = request.form['email']
#         user_pwd = request.form['password']
#         result = broker_userinfo.query.filter(broker_userinfo.user_email==email).first()
#         if result is None:
#             return redirect(url_for('error'))
#         user_id = result.user_id
#         user_name = result.user_name
#         if user_pwd == result.user_pwd:
#             return render_template('broker_userMenu.html', userid=user_id, username=user_name)

#GET brokerUserMenu Page
@app.route('/usermenu/<userid>', methods=['GET','POST'])
def broker_userMenu(userid):
    #if request.method == 'GET':
    username = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first().user_name
    return render_template('broker_userMenu.html', userid=userid, username=username)
    # else:
    #     username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
    #     return render_template('broker_userMenu.html', userid=userid, username=username)

#POST - brokerUserMenu Page
#compare pwd - login
# @app.route('/broker_main.html', methods=['POST'])
# def broker_login():
#     email = request.form['email']
#     user_pwd = request.form['password']
#     result = broker_userinfo.query.filter(broker_userinfo.user_email==email).first()
#     user_id = result.user_id
#     user_name = result.user_name
#     if user_pwd == result.user_pwd:
#         return render_template('broker_userMenu.html', userid=user_id, username=user_name)

#POST/GET - Submit Mortgage Application Form
#See all information
#Store information into table

# @app.route('/email_send.html', methods=['GET'])
# def email_send():
#     return render_template('/email_send.html')

#Reset Password
# @app.route('/broker_reset_password.html', methods=['GET', 'POST'])
# def reset():
#     if request.method == 'GET':
#         return render_template('broker_reset_password.html')
#     else:
#         email = request.form['email']
#         result = broker_userinfo.query.filter(broker_userinfo.user_email==email).first()
#         if result is not None:
#             message = "This email appears at here because you applied to reset your password are Zero Error Mortgage\n"
#             message += "Below is a link which can direct you to reset password\n"
#             msg = Message(message,
#                   sender="flooorence111@gmail.com",
#                   recipients=[str(email)])
#             mail.send(msg)
#             return render_template('email_send.html')
#         else:
#             return render_template('Error.html')


@app.route('/form/<userid>', methods=['GET','POST'])
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
        userMortgage = float(userMortgage)
        address = request.form['address']
        create_input = broker_mortgage_record(userid=userid, user_name=userRealName, usercompany=userCompany,
                                              userphone=userPhoneNum, useradd=userAddress, usermort=userMortgage, empid=empid,
                                              emp_name="None", emptitle="None", emp_dpt="None", usersalary=0, insurable=False,
                                              insurance=0, deductible=0, address=address, ins_company=None)
        if result is not None:   # update application detials
            result.user_realname = request.form['userRealName']
            result.user_company = request.form['userCompany']
            result.user_phone = request.form['userPhoneNum']
            result.user_address = request.form['userAddress']
            result.user_mortgage = request.form['userMortgage']
            result.emp_id = request.form['empID']
            result.address = request.form['address']
            db.session.commit()
            username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
            return redirect(url_for('broker_userMenu', userid=userid))
        else:   # create a new application
            db.session.add(create_input)
            db.session.commit()
            result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
            result.have_submitted = True
            db.session.commit()
            row = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first()
            token = hash(row.user_email)
            row.user_token = token
            db.session.commit()
            mortgageid = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first().mortgage_id
            return render_template('Confirmation.html', userid=userid, mortgageid=mortgageid, token=token)

@app.route('/Confirmation/<userid>', methods=['GET'])
def Confirmation(userid):
    username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
    return redirect(url_for('broker_userMenu', userid=userid))


@app.route('/brokerhome/<userid>', methods=['GET'])
def GoBack(userid):
    username = broker_userinfo.query.filter(broker_userinfo.user_id == userid).first().user_name
    return redirect(url_for('broker_userMenu', userid=userid))

#GET/POST - Authentication
@app.route('/authentication/<userid>', methods=['GET','POST'])
def broker_authentication(userid):
    row = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
    if request.method == 'GET' and row is not None:
        return render_template('broker_authentication.html',userid=userid)
    if request.method == 'GET' and row is None:
        return render_template('application.html', userid=userid)
    else:
        email = request.form['email']
        token = request.form['token']
        result = broker_userinfo.query.filter(broker_userinfo.user_email==email).first()
        if result.user_token==token and row is not None:
            return redirect(url_for('ApplicationInformation', userid=userid, row=row))
    return redirect(url_for('error'))

#GET - Mortgage Application Status
@app.route('/userstatus/<userid>', methods=['GET','POST'])
def broker_MortgageStatus(userid):
    result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
    result2 = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first()
    username = result2.user_name
    return render_template('user_status.html',userid=userid, rows=result, username=username)

#GET - Insurance Details
@app.route('/detail.html/<userid>', methods=['GET'])
def Insurance_Detail(userid):
    result = broker_mortgage_record.query.filter(broker_mortgage_record.user_id == userid).first()
    result2 = broker_userinfo.query.filter(broker_userinfo.user_id==userid).first()
    username = result2.user_name
    return render_template('insurance_detail.html',userid=userid, rows=result, username=username)

#GET/POST SignUp Page
@app.route('/signup', methods=['GET','POST'])
def SignUp():
    if request.method == 'GET':
        return render_template('broker_signUp.html')
    else:
        username = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        token = hash(email)
        create_input = broker_userinfo(name=username, pwd=pwd, email=email, token=token)
        db.session.add(create_input)
        db.session.commit()

        return render_template('broker_main.html')

#GET/POST forget token
@app.route('/newtoken/<userid>', methods=['GET'])
def ForgetToken(userid):
    broker_mortgage_record.query.filter(broker_mortgage_record.user_id==userid).delete()
    db.session.commit()
    #if request.method == 'GET':
    return redirect(url_for('ApplicationInformation', userid=userid))

@app.route('/deleteRecordConfirm/<userid>', methods=['GET'])
def delete_record_confirm(userid):
    return render_template('delete_prev_record_confirm.html', userid=userid)

@app.route('/employer/<userid>', methods=['GET','POST'])
def employer_letter(userid):
    mort = broker_mortgage_record.query.filter(broker_mortgage_record.user_id==userid).first()

    if request.method == 'GET':
        return render_template('employer_letter.html', userid=userid, row=mort)
    else:
        name = request.form['name']
        company = request.form['company']
        employer = request.form['employer']
        position = request.form['position']
        department = request.form['department']
        salary = int(request.form['salary'])
        #mort = broker_mortgage_record.query.filter(broker_mortgage_record.user_id==userid).first()
        mort.usercompany = company
        mort.employer_name = employer
        mort.employer_title = position
        mort.employer_dpt = department
        mort.user_salary = salary
        mort.have_emp_help = True
        db.session.commit()
        return redirect(url_for('broker_MortgageStatus', userid=userid))

@app.route('/insurance/<userid>', methods=['GET','POST'])
def insurance_letter(userid):
    mort = broker_mortgage_record.query.filter(broker_mortgage_record.user_id==userid).first()

    if request.method == 'GET':
        return render_template('insurance_letter.html', userid=userid, row=mort)
    else:
        name = request.form['name']
        company = request.form['company']
        address = request.form['address']
        insurance = request.form['insurance']
        deductive = request.form['deductive']
        #mort = broker_mortgage_record.query.filter(broker_mortgage_record.user_id==userid).first()
        mort.re_address = address
        mort.insurance_value = insurance
        mort.deductible_value = deductive
        mort.is_insurable = True
        mort.insurance_company = company
        db.session.commit()
        return redirect(url_for('broker_MortgageStatus', userid=userid))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)