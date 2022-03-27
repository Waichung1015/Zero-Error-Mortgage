from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pwd@127.0.0.1/broker'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '692898857938764',
        'secret': '15a98abf2d5e80f9b1ce6ca2f8bc531e'
    },
    'github':{
    	'id': 'd59d689142c87f1fa136',
    	'secret': '7a617be070b08391038cd17bec376d604c9c0bfb'
    }
}
app.config['SECRET_KEY'] = 'top secret!'

# app.config['MAIL_SERVER'] = 'stmp.google.com'
# app.config['MAIL_PORT'] = 