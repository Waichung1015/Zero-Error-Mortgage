from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

#connect to MySQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b65e280540657e:f1af7f27@us-cdbr-iron-east-03.cleardb.net/heroku_14b3224025d57d1'

#connect to MySQL from Local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usrname:pwd@ip/database_schema'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/real_estate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init orm database
db = SQLAlchemy(app)

class RE_info(db.Model):
    __tablename__ = 'RE_info'
    MIsID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_value = db.Column(db.Integer)
    property_years = db.Column(db.Integer),
    management_fee = db.Column(db.Numeric(12,2))
    purchased_time = db.Column(db.String(45))
    property_address = db.Column(db.String(45))
    manager = db.Column(db.String(45))
    def __init__(self, value, years, fee, time, manager, address):
        self.property_value = value
        self.property_years = years
        self.property_fee = fee
        self.management_fee = fee
        self.purchased_time = time
        self.manager = manager
        self.property_address = address


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
    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(45))
    name = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    property_address = db.Column(db.String(45))
    def __init__(self, email, name, phone, paddress):
        self.name = name
        self.user_email = email
        self.phone = phone
        self.property_address = paddress

#Get The Main Page For RE
@app.route('/', methods=['GET','POST'])
def RE_main():
    return render_template('RE/RE_main_page.html')

#GET/POST RE signup
@app.route('/RE/RE_signUp.html', methods=['GET','POST'])
def RE_signup():
    if request.method == 'GET':
        return render_template('RE/RE_signUp.html')
    else:
        user_name = request.form['un']
        pwd = request.form['pwd']
        email = request.form['email']
        create_input = RE_login(uname=user_name, email=email,pwd=pwd)
        db.session.add(create_input)
        db.session.commit()
        return render_template('RE/RE_main_page.html')

#GET/POST RE login
@app.route('/RE/RE_login.html', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('RE/RE_login.html')
    else:
        email = request.form['email']
        result = RE_login.query.filter(RE_login.user_email==email).first()
        userid = result.user_id
        row = RE_form.query.filter(RE_form.user_email==email).first()
        pwd = request.form['pwd']
        print(userid)
        if pwd == result.user_pwd:
            if row is None:
                return render_template('RE/RE_form.html', result=result, userid=userid)
            else:
                #form_id = row.form_id
                name = result.user_name
                return render_template('RE/RE_formreview.html', username=name, rows=row, userid=userid)

#GET/POST RE Form
@app.route('/RE/RE_form.html/<userid>', methods=['GET','POST'])
def form(userid):
    result = RE_login.query.filter(RE_login.user_id==userid).first()
    row = RE_form.query.filter(RE_form.user_email==result.user_email).first()
    if request.method == 'GET':
        return render_template('RE/RE_form.html' )
    else:
        name = request.form['Name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        if row is None:
            #result = RE_info.query.filter(RE_info.property_address == address).first()
            #property_value = result.property_value
            create_input = RE_form(name=name, email=email, phone=phone, paddress=address)
            db.session.add(create_input)
            db.session.commit()
            return render_template('RE/RE_confirmation.html')
        else:
            # result = RE_info.query.filter(RE_info.MIsID == MIsID).first()
            # property_value = result.property_value
            # db.session.commit()
            # insurance = random.randint(int(property_value / 3), int(property_value / 2))
            # deductible = property_value - insurance
            # newdata = Insurance_info(insurance=insurance, deductible=deductible, name=name, property=property_value,
            #                          insurable=True,
            #                          reid=userid)
            # db.session.add(newdata)
            # db.session.commit()
            # new = Insurance_info.query.filter(Insurance_info.re_id == userid).first()
            # insurance_id = new.ID
            # result2 = broker_mortgage_record.query.filter(broker_mortgage_record.mortgage_id == mortgage_id).first()
            # result2.ID = insurance_id
            row.user_email = email
            row.phone = phone
            row.name = name
            row.property_address = address
            db.session.commit()
            return render_template('RE/RE_confirmation.html')
#Get The Main Page For RE
@app.route('/RE/RE_confirmation.html', methods=['GET'])
def RE_confirmation():
    return render_template('RE/RE_confirmation.html')


if __name__ == '__main__':
    app.run(debug=True)