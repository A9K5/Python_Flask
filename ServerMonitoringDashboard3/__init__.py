from flask import Flask
from cpustat.views import CPUSTAT
# from ufwrules.views import ufwrules_blueprint
from mongostat.views import MongoStat
from awss3.views import AWSS3
# from UfwR.views import UfwR

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

# This one matches urls like: http://socool.biz/api/...
CPUSTAT.register(app, route_base='/cpu/')
MongoStat.register(app, route_base='/mongsta/')
AWSS3.register(app, route_base='/awss3/')

# UfwR.register(app, route_base='/ufw/')
# app.register_blueprint(ufwrules_blueprint,url_prefix='/ufww/')


# This one matches urls like: http://api.socool.biz/...
# CPUSTAT.register(app, route_base='/abc', subdomain='api')

if __name__ == "__main__":
    app.run(debug=True)



# Running with Gunicon
#   gunicorn -w 4 __init__:app    