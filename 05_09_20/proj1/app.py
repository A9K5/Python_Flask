from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

def token_required(f):
    @wraps(f)
    def decorated( *args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message':'Token not found'}),403

        try:
            jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':' Token is invalid'}),403
        
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@token_required 
def protected():
    return jsonify({'message':'Protected view'})

@app.route('/unprotected') 
def  unprotected():
    return jsonify({'message':'Un-Protected view'})


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({ 'user':auth.username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=10*60 )},app.config['SECRET_KEY'])
        return jsonify( {'token':token.decode('UTF-8')} )

    return make_response('Could\'nt verfiy',401,{'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == "__main__":
    app.run(debug=True)


# http://127.0.0.1:5000/login
# http://127.0.0.1:5000/unprotected
# http://127.0.0.1:5000/protected?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYmxhaCIsImV4cCI6MTU5OTI1NjExMX0.h972ZB3GZsxc-ek9ZRnm8dhtQZXzG4LkQ-L0AlyTmxM