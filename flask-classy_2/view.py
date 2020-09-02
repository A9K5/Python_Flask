from flask_classy import FlaskView

class CoolApiView(FlaskView):
    subdomain = "api"

    def index(self):
        return "API Stuff"