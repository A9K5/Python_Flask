from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = "Thisissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/ankurkumar/Documents/Git/Python_Flask/12_09_20/data.db"

db = SQLAlchemy(app)

subs = db.Table('subs',
            db.Column('user_id',db.Integer, db.ForeignKey("user.user_id"),primary_key=True),
            db.Column('channel_id',db.Integer,db.ForeignKey("channel.channel_id"),primary_key=True)
            )

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))            
    subscriptions = db.relationship('Channel',secondary='subs', backref=db.backref('subscribers',lazy='dynamic'))


class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20))




# >>> from many import *
# /Users/ankurkumar/Documents/Git/Python_Flask/03_09_20/venv/lib/python3.8/site-packages/flask_sqlalchemy/__init__.py:833: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
#   warnings.warn(FSADeprecationWarning(
# >>> db.create_all()
# >>> user1 = User(name="Ankur")
# >>> user2 = User(name="Stan")
# >>> user3 = User(name="Ron")
# >>> db.session.add(user1)
# >>> db.session.add(user2)
# >>> db.session.add(user3)
# >>> db.commit_all()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'SQLAlchemy' object has no attribute 'commit_all'
# >>> db.commit()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'SQLAlchemy' object has no attribute 'commit'
# >>> db.session.commit()
# >>> cha1 = Channel(channel_name='TeaTime')
# >>> cha2 = Channel(channel_name='CofeeTime')
# >>> cha3 = Channel(channel_name='ExpressoTime')
# >>> db.session.add(cha1)
# >>> db.session.add(cha2)
# >>> db.session.add(cha3)
# >>> db.session.commit()
# >>> cha1.subscribers.append(user1)

# try:
# ...     db.session.commit()
# ... except:
# ...     db.session.rollback()