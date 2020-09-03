from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,  UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ankurkumar/Documents/Git/Python_Flask/03_09_20/proj1/login.db'
app.config['SECRET_KEY'] = "Thisissercret"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    user = User.query.filter_by(username='Anthony').first()
    login_user(user)
    return "You r logged in. "


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You r noew logged out"

@app.route('/home')
@login_required
def home():
    return ("Current User "+ current_user.username)
     

if __name__=='__main__':
    app.run(debug=True)