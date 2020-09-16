from flask import Flask, request, jsonify, make_response, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid  
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from bs4 import BeautifulSoup
import requests
import json


from flask_restful import Api
from flask_jwt_extended import (JWTManager, jwt_required, 
                                jwt_refresh_token_required, 
                                jwt_optional, fresh_jwt_required, 
                                get_raw_jwt, get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies,unset_access_cookies)
                                

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/ankurkumar/Documents/Git/Python_Flask/12_09_20/proj1/user.db"

app.config['BASE_URL'] = 'http://127.0.0.1:5000' 
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True
jwt = JWTManager(app) 


db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))


class Movie(db.Model):
    movie_id = db.Column(db.String(50))
    movie_name = db.Column(db.String(20),primary_key=True)
    watched = db.Column(db.Boolean,default=False)
    user_id = db.Column(db.Integer,primary_key=True) 

    genre = db.Column(db.String(20))
    director_name = db.Column(db.String(50))
    thumbnailUrl = db.Column(db.String(100))
    duration = db.Column(db.String(10))
    rating = db.Column(db.String(4))
    date_published = db.Column(db.String(10))
    description = db.Column(db.String(200))




def assign_access_refresh_tokens(user_id, url):
    # access_token = create_access_token(identity=str(user_id))
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    resp = make_response(redirect(url, 302))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

def unset_jwt():
    resp = make_response(redirect(app.config['BASE_URL'] + '/', 302))
    unset_jwt_cookies(resp)
    return resp


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    return redirect(app.config['BASE_URL'] + '/loginpage', 302)

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect(app.config['BASE_URL'] + '/loginpage'))
    unset_jwt_cookies(resp)
    return resp, 302

@jwt.expired_token_loader
def expired_token_callback(callback):
    # Expired auth header
    resp = make_response(redirect(app.config['BASE_URL'] + '/loginpage'))
    unset_access_cookies(resp)
    return resp, 302


@app.route('/',methods=['GET'])
def show():
    return render_template('login.html')


@app.route('/loginpage',methods=['GET'])
def loginpage():
    return render_template('login.html')




@app.route('/login',methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(name=username).first()
    print(username,password)
    if not user:
        return unset_jwt(), 302
        # return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login Required!"' })

    if check_password_hash(user.password,password):
        # token = jwt.encode({'public_id':user.public_id , 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=40)},app.config['SECRET_KEY'])

        return  assign_access_refresh_tokens(user.user_id , app.config['BASE_URL'] + '/show')


    return unset_jwt(), 302
    # return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login Required!"' })

@app.route('/logout',methods=['GET'])
@jwt_required
def logout():
    # Revoke Fresh/Non-fresh Access and Refresh tokens
    return unset_jwt(), 302




    
@app.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()
    # print(data)
    hashed_password = generate_password_hash( data["password"], method='sha256')
    # print(hashed_password)
    new_user = User( public_id = str(uuid.uuid4()), name = data['name'], password = hashed_password )
    db.session.add(new_user)
    db.session.commit()

    return jsonify( {'message':'New user Created . '})

@app.route('/add_playlist',methods=['POST','GET'])
def add_playlist():
    print(request.form['link'])
    # Do calculation and addition
    return redirect(url_for('show_movie'))
    # return jsonify({"message":'Playlist addded'})



@app.route('/add_list', methods=['GET'])
@jwt_required
def add_list():
    # add the parser for movies data over here. and then put the whole data using the below code.
    # data = request.get_json()
    user_public_id = get_jwt_identity()
    print(user_public_id)
    def get_ld_json(url: str) -> dict:
        parser = "html.parser"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, parser)
        return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

    print(str(request.args['movie_name']))
    d = get_ld_json(str(request.args['movie_name']))
        # request.form['link'])
    # print(d)
    print(d['genre'])
    print(d['name'])
    # print(d['director']['name'])
    print(d['duration'])

    data = {}
    data['name'] = d['name']
    data['genre'] = " ".join(d['genre'])
    if type(d['director'])==dict:
        data['director_name'] = d['director']['name']
    else:
        data['director_name'] = d['director'][0]['name']

    data['thumbnailUrl'] = d['trailer']['thumbnailUrl']
    data['duration'] = d['duration'][2:]
    data['rating'] = d['aggregateRating']['ratingValue']
    data['date_published']=d['datePublished'][:4]
    data['description'] = d['description'][:100]
    
    data['user_id'] = user_public_id
    # int(request.form['user_id'])
    
    print(data)
    # return jsonify(data)
    try:
        new_movie = Movie(movie_name=data['name'],
                        user_id = data['user_id'], 
                        watched=False, 
                        movie_id=str(uuid.uuid4()), 
                        
                        genre = data['genre'],
                        director_name = data['director_name'],
                        thumbnailUrl = data['thumbnailUrl'],
                        duration = data['duration'],
                        rating = data['rating'],
                        date_published = data['date_published'],
                        description = data['description']                        

                        )   
        db.session.add(new_movie)
        db.session.commit() 
        return redirect(url_for('show_movie'))

        # jsonify( {'message':'New movie Created . '})
    
    
    except:
        db.session.rollback()
        return redirect(url_for('show_movie'))
    
        # jsonify( {'message':'Movie already exist for the user. '})

    
    # return redirect(url_for('show_movie'))

    # print(data)
    # try:
    #     new_movie = Movie(movie_name=data['name'],user_id = data['user_id'], watched=False, movie_id=str(uuid.uuid4()) )   
    #     db.session.add(new_movie)
    #     db.session.commit() 
    #     return jsonify( {'message':'New movie Created . '})
    # except:
    #     db.session.rollback()
    #     return jsonify( {'message':'Movie already exist for the user. '})
        # all ok now




# working fine
@app.route('/show',methods=['GET'])
@jwt_required
def show_movie():
    user_public_id = get_jwt_identity()
    data = Movie.query.filter_by(user_id=user_public_id)
    post = []
    for d in data:
        post.append( { "movie_name":d.movie_name, 
                    "watched":d.watched, 
                    "user_id": d.user_id,
                    "drama": "Updated Later", 
                    "movie_id":d.movie_id  ,
                    "genre":d.genre,
                    "director_name":d.director_name,
                    "thumbnailUrl":d.thumbnailUrl,
                    "rating":d.rating,
                    "date_published":d.date_published,
                    "description":d.description
                    } )
    # post = [
    #     {
    #         "movie_id":1,
    #         "movie_name":"Pirates of Carribean",
    #         "description":" DRAMA"
    #     },
    #     {
    #         "movie_id":10,
    #         "movie_name": "Sherlock",
    #         "description": "Adventure"
    #     }
    # ]
    return render_template('page.html',posts=post)

@app.route('/watched',methods=['GET'])
@jwt_required
def watched():
    user_public_id = get_jwt_identity()
    data = Movie.query.filter_by(user_id=user_public_id, watched=True)
    post = []
    for d in data:
        post.append( { "movie_name":d.movie_name, "watched":d.watched, "user_id": d.user_id,"drama": "Updated Later", "movie_id":d.movie_id  } )

    return render_template('page.html',posts=post)

@app.route('/binge',methods=['GET'])
@jwt_required
def binge():
    user_public_id = get_jwt_identity()
    data = Movie.query.filter_by(user_id=user_public_id, watched=False)
    post = []
    for d in data:
        post.append( { "movie_name":d.movie_name, "watched":d.watched, "user_id": d.user_id,"drama": "Updated Later", "movie_id":d.movie_id  } )

    return render_template('page.html',posts=post)

@app.route('/<string:id>/mark_watched',methods=['GET'])
@jwt_required
def mark_watched(id):
    print(id)
    if request.method=='GET':
        data = Movie.query.filter_by(movie_id=id).first()#.update(watched=True)
        data.watched=True
        # db.session.update(data)
        db.session.commit()
        return redirect(url_for('show_movie'))


    # return render_template()








if __name__ == "__main__":
    app.run(debug=True)