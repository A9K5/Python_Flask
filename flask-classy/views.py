
from flask_classy import FlaskView, route

class CoolApiView(FlaskView):

    def index(self):
        return "API stuff"

    @route('/show/')
    def show(self):
        return "Show API"