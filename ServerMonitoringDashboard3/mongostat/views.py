from flask_classy import FlaskView, route
from pymongo import MongoClient
import os
import json

class MongoStat(FlaskView):

    def index(self):
        return "API stuff"

    @route('/show/')
    def show(self):
        return "Show API"

    # Done
    @route('/mongostat/', methods=['GET'])
    def mongostat(self):
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
    @route('/mongouser/', methods=['GET'])
    def mongouser(self):
        conn = MongoClient()
        db = conn.iotdash4
        listing = db.command('usersInfo')
        print(listing)
        return json.dumps(listing)
