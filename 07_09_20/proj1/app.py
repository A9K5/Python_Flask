from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user



app = Flask(__name__)

app.config['SECRET_KEY'] = "Thisissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/ankurkumar/Documents/Git/Python_Flask/07_09_20/proj1/login.db"

twitter_blueprint = make_twitter_blueprint(api_key='',api_secret='')

app.register_blueprint(twitter_blueprint,url_prefix='/twitter_login')

db = SQLAlchemy(app)
login_manager = LoginManager(app)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250),unique=True)

class OAuth(OAuthConsumerMixin,db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

twitter_blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user,user_required=False)
# user_required=False has worked over here but it should not be used.

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')
    
    account_info_json = account_info.json()
    return 'YOur twitter name is @{}'.format(account_info_json['screen_name'])


@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):
    account_info = blueprint.session.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['screen_name']
        
        query = User.query.filter_by(username=username)
        
        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            

        login_user(user)

# @app.route('/twitter')
# def twitter_login():
#     if not twitter.authorized:
#         return redirect(url_for('twitter.login'))
#     account_info = twitter.get('account/settings.json')
    
#     if account_info.ok:
#         account_info_json = account_info.json()
#         return 'YOur twitter name is @{}'.format(account_info_json['screen_name'])

#     return 'Request failed!.'

# @oauth_authorized.connect_via(twitter_blueprint)
# def twitter_logged_in(blueprint, token):
#     if not token:
#         flash("Failed to log in.", category="error")
#         return False

#     resp = blueprint.session.get("account/verify_credentials.json")
#     if not resp.ok:
#         msg = "Failed to fetch user info."
#         flash(msg, category="error")
#         return False

#     info = resp.json()
#     user_id = info["id_str"]

#     # Find this OAuth token in the database, or create it
#     query = OAuth.query.filter_by(
#         provider=blueprint.name,
#         provider_user_id=user_id,
#     )
#     try:
#         oauth = query.one()
#     except NoResultFound:
#         oauth = OAuth(
#             provider=blueprint.name,
#             provider_user_id=user_id,
#             token=token,
#         )

#     if oauth.user:
#         login_user(oauth.user)
#         flash("Successfully signed in.")

#     else:
#         # Create a new local user account for this user
#         user = User(
#             name=info["screen_name"],
#         )
#         # Associate the new local user account with the OAuth token
#         oauth.user = user
#         # Save and commit our database models
#         db.session.add_all([user, oauth])
#         db.session.commit()
#         # Log in the new local user account
#         login_user(user)
#         flash("Successfully signed in.")

#     # Disable Flask-Dance's default behavior for saving the OAuth token
#     return False



@app.route('/')
@login_required
def index():
    return "you are logged in as {}".format(current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return  redirect(url_for('index')) 

if __name__ == "__main__":
    app.run(debug=True)