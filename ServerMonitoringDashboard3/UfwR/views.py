from flask_classy import FlaskView, route
# import ufww as ufw
import json
import ufww as ufo

class UfwR(FlaskView):

    def index(self):
        return "API stuff"

    @route('/show/')
    def show(self):
        print(ufo.status())
        status = {
            "status": str(ufo.status())
        }
        return json.dumps(status)
