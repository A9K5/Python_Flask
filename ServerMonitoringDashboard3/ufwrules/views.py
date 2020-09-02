# import easyufw as ufw
from flask_classy import FlaskView, route
from flask import request,Blueprint
import json

ufwrules_blueprint = Blueprint('ufwrules', __name__)
# ___________________________________________
# ____________________________________________

@ufwrules_blueprint.route('/status/', methods=['GET'])
def ufww():
    import ufww
    print(ufww.status())
    status = {
        "status": str(ufww.status())
    }
    return json.dumps(status)

@ufwrules_blueprint.route('/allow/proc/', methods=['POST'])
def allowproc():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    protocol = dataDict["protocol"]
    import ufww as ufw
    ufw.allow(port, protocol)
    return json.dumps({"Status": "OK"})

# Done
@ufwrules_blueprint.route('/allow/', methods=['POST'])
def allow():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    import ufww as ufw
    ufw.allow(port)
    return json.dumps({"Status": "OK"})

# Done
@ufwrules_blueprint.route('/deny/proc/', methods=['POST'])
def denyproc():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    protocol = dataDict["protocol"]
    import ufww as ufw
    ufw.deny(port, protocol)
    return json.dumps({"Status": "OK"})

# Done
@ufwrules_blueprint.route('/deny/', methods=['POST'])
def deny():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    import ufww as ufw
    ufw.deny(port)
    return json.dumps({"Status": "OK"})

# Not to used for security purposes

# @ufwrules_blueprint.route('/delete/',methods=['POST'])
# def delete():
#     data = (request.data.decode('utf-8'))
#     dataDict = json.loads(data)
#     port = dataDict["port"]
#     import ufww as ufw
#     ufw.delete(port)
#     return json.dumps({"Status":"OK"})
