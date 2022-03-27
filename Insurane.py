from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#connect to MySQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b65e280540657e:f1af7f27@us-cdbr-iron-east-03.cleardb.net/heroku_14b3224025d57d1'

#connect to MySQL from Lacal
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usrname:pwd@ip/database_schema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init orm database
db = SQLAlchemy(app)

#tables
#application form
class Insurance_application(db.Model):
    __tablename__ = 'Insurance_application'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45))
    re_address = db.Column(db.String(64))
    re_value = db.Column(db.Integer)
    work_company = db.Column(db.String(45))
    work_depart = db.Column(db.String(45))
    work_salary = db.Column(db.Numeric(12,2))
    has_reviewed = db.Column(db.Boolean, default=False)
    reviewed_by  = db.Column(db.String(45))
    reviewed_result = db.Column(db.String(45))

    def __init__(self, name, address, value, company, depart, salary, has_reviewed, reviewed_by, result):
        self.name = name
        self.re_address = address
        self.re_value = value
        self.work_company = company
        self.work_depart = depart
        self.work_salary = salary
        self.has_reviewed = has_reviewed
        self.reviewed_by = reviewed_by
        self.reviewed_result = result

class Insurance_info(db.Model):
    __tablename__ = 'Insurance_info'
    insurance_value = db.Column(db.Numeric(12,2))
    deductible_value = db.Column(db.Numeric(12,2))
    property_address = db.Column(db.String(64))
    name = db.Column(db.String(45))
    ID = db.Column(db.Integer, db.ForeignKey('Insurance_application.ID'), primary_key=True)
    property_value = db.Column(db.Integer)
    is_insurable = db.Column(db.Boolean, default=False)
    def __init__(self, insurance, deductible, name, Property, insurable, address, ID):
        self.insurance_value = insurance
        self.deductible_value = deductible
        self.name = name
        self.property_value = Property
        self.is_insurable = insurable
        self.property_address = address
        self.ID = ID

#get the Home Page for Insurance portal
@app.route('/', methods=['GET'])
def Home():
    return render_template('Insurance/Insinc_query.html')

@app.route('/confirm', methods=['GET'])
def confirm():
    return render_template('Insurance/application_comfirmation.html')

#apply for an insurance
@app.route('/apply', methods=['GET', 'POST'])
def insurance_apply():
    if request.method == 'GET':
        return render_template('Insurance/Insurance_application.html')
    else:
        insurance_value, deductible_value = 0, 0
        name = request.form['name']
        address = request.form['address']
        value = request.form['value']
        company = request.form['company']
        department = request.form['department']
        salary = request.form['salary']
        reviewed_by = request.form['reviewed_com']
        reviewed_result = request.form['result']
        has_reviewed = request.form.get('reviewed')
        if has_reviewed == "yes":
            has_reviewed = True
            insurance_value = 1000
            deductible_value = 1000
        else:
            has_reviewed = False
        input1 = Insurance_application(name=name, address=address, value=value, company=company, 
            depart=department, salary=salary, has_reviewed=has_reviewed, reviewed_by=reviewed_by, result=reviewed_result)
        db.session.add(input1)
        db.session.commit()
        ID = Insurance_application.query.filter(Insurance_application.re_address==address and Insurance_application.name==name).first().ID
        print(ID)
        if insurance_value != 0 and deductible_value != 0:
            insurance = Insurance_info(insurance=insurance_value, deductible=deductible_value, 
                name=name, Property=value, insurable=True, address=address, ID=ID)
            db.session.add(insurance)
            db.session.commit()
        return redirect(url_for('confirm'))


@app.route('/', methods=['POST'])
def insurance_search():
    address = request.form['address']
    name = request.form['name']
    rows = Insurance_info.query.filter(Insurance_info.name==name and Insurance_info.property_address==address).first()
    if rows is not None:
        return render_template('Insurance/result.html', rows=rows)
    else:
        return render_template('Insurance/error.html')

if __name__ == '__main__':
    app.run(debug=True)
