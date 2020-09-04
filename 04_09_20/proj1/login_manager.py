from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import  URLSafeSerializer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/ankurkumar/Documents/Git/Python_Flask/04_09_20/proj1/user.db'
app.config['SECRET_KEY'] = 'This is secret Key'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

serializer = URLSafeSerializer(app.secret_key)

class User( UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True)
    password =  db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self):  
        return str(self.session_token) 

@login_manager.user_loader
def load_user(session_token):
    return User.query.filter_by(session_token=session_token).first()
     

def create_user():
    user = User(username="Anthony", password="password1", session_token=serializer.dumps(["Anthony","password1"]))
    db.session.add(user)
    db.session.commit()

def update_token():
    anthony = User.query.filter_by(username='Anthony').first()
    anthony.password = 'password2'
    anthony.session_token = serializer.dumps(["Anthony","password2"])
    db.session.commit()


@app.route('/')
def index():
    user = User.query.filter_by(username='Anthony').first() 
    login_user(user, remember=True)
    return "You are now logged in."

@app.route('/home')
@login_required
def home():
    return "The current user is"+ current_user.username

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are now logged out."

if __name__=='__main__':
    app.run(debug=True)