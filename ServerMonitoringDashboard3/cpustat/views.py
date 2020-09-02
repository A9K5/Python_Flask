from flask_classy import FlaskView, route
from flask import request
import json

class CPUSTAT(FlaskView):

    def index(self):
        return "API stuff"

    @route('/show/')
    def show(self):
        return "Show API"

    @route('/cpustat/dict/', methods=['POST']) # with limit in the query 
    def cpustatdict(self):
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

    @route('/cpuusers/', methods=['GET'])
    def cpuusers(self):
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

    @route('/cpupid/',methods=['GET'])
    def cpupid(self):
        import psutil
        procs = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username'])}
        return json.dumps(procs)