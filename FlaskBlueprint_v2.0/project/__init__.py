from flask import Flask
# -*- coding: utf-8 -*-

app = Flask(__name__)
# from . import views

from project.users.views import users_blueprint
from project.recepies.views import recepies_blueprint

app.register_blueprint(users_blueprint,url_prefix='/pages')
app.register_blueprint(users_blueprint,url_prefix='/pa')
app.register_blueprint(recepies_blueprint)
