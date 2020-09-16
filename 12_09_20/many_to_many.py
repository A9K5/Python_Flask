from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = "Thisissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/ankurkumar/Documents/Git/Python_Flask/12_09_20/database.db"

db = SQLAlchemy(app)

subs = db.Table('subs',
            db.Column('user_id',db.Integer, db.ForeignKey("user.user_id")),
            db.Column('channel_id',db.Integer,db.ForeignKey("channel.channel_id"))
            )

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))            
    subscriptions = db.relationship('Channel',secondary='subs', backref=db.backref('subscribers',lazy='dynamic'))


class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20))

