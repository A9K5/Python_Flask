from flask import Flask
from views import CoolApiView

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

# This one matches urls like: http://socool.biz/api/...
# CoolApiView.register(app, route_base='/api/')

# This one matches urls like: http://api.socool.biz/...
CoolApiView.register(app, route_base='/', subdomain='api')

if __name__ == "__main__":
    app.run()