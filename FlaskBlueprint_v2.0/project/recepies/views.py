from flask import render_template, Blueprint

recepies_blueprint = Blueprint('recepies',__name__,template_folder='templates')

@recepies_blueprint.route('/')
def index():
    return render_template('index.html')