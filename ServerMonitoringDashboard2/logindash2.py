from flask import Flask, request, session, redirect, url_for, render_template
import boto3
import random
import string
import json


app = Flask(__name__)

# Use classes,blueprints in different files bas and done... 

@app.route('/')
def index():
    return "BLAH!!"

# Done
# @app.route('/cpustat/', methods=['POST']) # with limit in the query 
# def cpustat():
#     data = (request.data.decode('utf-8'))
#     dataDict = json.loads(data)
#     lim = dataDict["limit"]
#     finmsg = []
#     from pymongo import MongoClient
#     conn = MongoClient()
#     db = conn.iotdash5
#     cursor = db.alluse.find({}, {"_id": 0}).sort('_id', -1).limit(lim)
#     data = [x for x in cursor] # Output with count as in aws dynamodb
#     finmsg.append(data)
#     finmsg.append({"Count":len(data)})
#     # print (finmsg)
#     return json.dumps(finmsg)

# Done
@app.route('/cpustat/dict/', methods=['POST']) # with limit in the query 
def cpustatdict():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    lim = dataDict["limit"]
    finmsg = {}
    from pymongo import MongoClient
    conn = MongoClient()
    db = conn.iotdash5
    cursor = db.alluse.find({}, {"_id": 0}).sort('_id', -1).limit(lim)
    data = [x for x in cursor] # Output with count as in aws dynamodb
    finmsg["Items"] = data
    finmsg["Count"]= len(data)
    # print (finmsg)
    return json.dumps(finmsg)

# Done
@app.route('/cpuusers/', methods=['GET'])
def cpuusers():
    import psutil
    msg=[]
    finmsg={}
    for c in psutil.users():
        msg.append({
            "name":c.name,
            "terminal":c.terminal,
            "host":c.host,
            "started":c.started,
            "pid":c.pid
        })
    finmsg["Items"] = msg
    finmsg["Count"] = len(msg)
    return json.dumps(finmsg)

# Done
@app.route('/cpupid/',methods=['GET'])
def cpupid():
    import psutil
    procs = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username'])}
    return json.dumps(procs)


# Done
@app.route('/ufww/status/',methods=['GET'])
def ufww():
    import easyufw as ufw
    print(ufw.status())
    status = {
        "status": str(ufw.status()) 
    }
    return json.dumps(status)

# Done
@app.route('/ufww/allow/proc/',methods=['POST'])
def allowproc():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    protocol = dataDict["protocol"]
    import easyufw as ufw
    ufw.allow(port,protocol)
    return json.dumps({"Status":"OK"})

# Done
@app.route('/ufww/allow/',methods=['POST'])
def allow():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    import easyufw as ufw
    ufw.allow(port)
    return json.dumps({"Status":"OK"})

# Done
@app.route('/ufww/deny/proc/',methods=['POST'])
def denyproc():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    protocol = dataDict["protocol"]
    import easyufw as ufw
    ufw.deny(port,protocol)
    return json.dumps({"Status":"OK"})

# Done
@app.route('/ufww/deny/',methods=['POST'])
def deny():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    port = dataDict["port"]
    import easyufw as ufw
    ufw.deny(port)
    return json.dumps({"Status":"OK"})

# Not to used for security purposes

# @app.route('/ufww/delete/',methods=['POST'])
# def delete():
#     data = (request.data.decode('utf-8'))
#     dataDict = json.loads(data)
#     port = dataDict["port"]
#     import easyufw as ufw
#     ufw.delete(port)
#     return json.dumps({"Status":"OK"})

# Done
@app.route('/netconnections/',methods=['GET'])
def netconnections():
    import socket
    from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
    import psutil
    AD = "-"
    AF_INET6 = getattr(socket, 'AF_INET6', object())
    proto_map = {
        (AF_INET, SOCK_STREAM): 'tcp',
        (AF_INET6, SOCK_STREAM): 'tcp6',
        (AF_INET, SOCK_DGRAM): 'udp',
        (AF_INET6, SOCK_DGRAM): 'udp6',
    }
    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    print(templ % (
        "Proto", "Local address", "Remote address", "Status", "PID",
        "Program name"))
    proc_names = {}
    jsonmsg = []
    for p in psutil.process_iter(attrs=['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']
    for c in psutil.net_connections(kind='inet'):
        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)
        jsonmsg.append({"Proto": proto_map[(c.family, c.type)],
                        "Local address": laddr,
                        "Remote address": raddr or AD,
                        "Status": c.status,
                        "PID": c.pid or AD,
                        "Program name": proc_names.get(c.pid, '?')[:15]
                        })
    return json.dumps(jsonmsg)




# Done
@app.route('/mongostat/', methods=['GET'])
def mongostat():
    import os
    msg = {}
    v = 'service mongod status > mongodstat.txt'
    os.system(v)
    f = open("mongodstat.txt", "r")
    fi = f.readlines()
    for x in fi:
        if x.find('Active') > 0:
            msg['Active'] = x[x.find('Active')+8:-1]
        elif x.find('Main PID') > 0:
            msg['Main PID'] = x[x.find('Main PID')+10:-1]
        elif x.find('Tasks') > 0:
            msg['Tasks'] = x[x.find('Tasks')+7:-1]
        elif x.find('Memory') > 0:
            msg['Memory'] = x[x.find('Memory')+8:-1]
        elif x.find('CPU') > 0:
            msg['CPU'] = x[x.find('CPU')+5:-1]
        elif x.find('CGroup') > 0:
            msg['CGroup'] = x[x.find('CGroup')+8:-1]
        elif x.find('Loaded') > 0:
            msg['Loaded'] = x[x.find('Loaded')+8:-1]

    print(msg)
    return json.dumps(msg)

# Done
@app.route('/monogouser/',methods=['GET'])
def mongouser():
    from pymongo import MongoClient
    conn = MongoClient()
    db = conn.iotdash4 
    listing = db.command('usersInfo')
    print (listing)
    return json.dumps(listing)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)  # , host="192.168.43.140")
