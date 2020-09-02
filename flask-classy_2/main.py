from flask import Flask
from view import CoolApiView

app = Flask(__name__)
app.config['SERVER_NAME'] = 'socool.biz'

# This one matches urls like: http://socool.biz/api/...
# CoolApiView.register(app, route_base='/api/', subdomain='')

# This one matches urls like: http://api.socool.biz/...
CoolApiView.register(app, route_base="/")

if __name__ == "__main__":
    app.run()
