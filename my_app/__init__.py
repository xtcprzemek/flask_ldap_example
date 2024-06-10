from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['LDAP_PROVIDER_URL'] = 'ldap://localhost:389/'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)
 
app.secret_key = 'some_random_key'
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
 
from my_app.auth.views import auth
app.register_blueprint(auth)
 
db.create_all()