from flask import Blueprint, render_template

users_blueprint = Blueprint('users', __name__, template_folder='templates',url_prefix='/a/')

@users_blueprint.route('/login/')
def login():
    return render_template('login.html')

@users_blueprint.route('/asdf/pwd/')
def login2():
    return ("hello")