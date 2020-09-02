from flask import Flask, render_template
# from pymongo import MongoClient
from connectionMongo import db

import gviz_api
import json
import psutil


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('newfreqchart.html')


@app.route('/chart/')
def chart():
    description = {"threads": ("string", "Threads"),
                   "cpuusage": ("number", "Cpu Usage")}

    cursor = db.users.find({}, {"_id": 0, "threads": 1, "cpuusage": 1})
    data = [x for x in cursor]
    # print(data)
    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Create a JavaScript code string.
    # jscode = data_table.ToJSCode("jscode_data", columns_order=(
    #     "name", "salary"), order_by="salary")
    # Create a JSON string.
    json1 = data_table.ToJSon(columns_order=(
        "threads", "cpuusage"), order_by="cpuusage")

    return (json1)


@app.route('/cpu')
def cpu():
    cputime = psutil.cpu_percent()
    db.users.insert_one({"cpuusage": cputime})
    return(cputime)


@app.route('/cpuperformance/')
def cpuperformance():
    description = {"time": ("number", "Cpu Usage Percentage"),
                   "cpuusage": ("number", "Cpu Usage")}
    cursor = db.cpuusage.find(
        {}, {"_id": 0, "time": 1, "cpuusage": 1}).sort('_id', -1).limit(20)
    data = [x for x in cursor]
    # print(data, '->')

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    json1 = data_table.ToJSon(columns_order=(
        "time", "cpuusage"), order_by="time")
    # print(json1)
    return json1


@app.route('/cpufreq/')
def cpufreq():
    description = {"time": ("number", "Time"),
                   "freq1": ("number", "Freq 1"),
                   "freq2": ("number", "Freq2"),
                   "freq3": ("number", "Freq3"),
                   "freq4": ("number", "Freq4")}
    cursor = db.frequse.find(
        {}, {"time": 1, "freq1": 1, "freq2": 1, "freq3": 1, "freq4": 1}).sort('_id', -1).limit(10)
    data = [x for x in cursor]
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    json1 = data_table.ToJSon(columns_order=(
        "time", "freq1", "freq2", "freq3", "freq4"), order_by="time")
    print(json1)
    return json1


if __name__ == "__main__":
    app.run(debug=True,host="192.168.43.140")
