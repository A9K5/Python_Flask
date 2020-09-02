from __future__ import print_function
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import botocore
import boto3
import decimal
import logging
import time
import argparse
import json
import random
import string
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')#, region_name='us-west-2', endpoint_url="http://localhost:8000")
table = dynamodb.Table('IOT4')
AllowedActions = ['both', 'publish', 'subscribe']

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/test',methods=['GET'])
@cross_origin()
def test():
    return "hello"

@app.route('/test/post',methods=['POST'])
@cross_origin()
def testPost():
    # print(json.dumps(request.data))
    print(request.form)
    print(request.values)
    print(request.headers)
    return "hello"

@app.route('/create1',methods=['POST'])
def student():
    id = request.values.get('id')
    name = request.values.get('name')
    email = request.values.get('email')
    contactno = request.values.get('contactno')
    response = table.put_item(
        Item={
            '_id':  datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'ID': id ,
            'NAME1': name,
            'EMAIL': email,
            'CONTACTNO': contactno,
            'ADDRESS': {}
        }
    )
    print(response)
    return redirect('/')
    
@app.route('/newupdate' , methods = ['GET'])
def newupdate():
    id = request.values.get("_id")
    #task = collection.find({"_id":ObjectId(id)})
    task = table.query(
        ProjectionExpression = "#id , ID , #ame , EMAIL , CONTACTNO ",
        ExpressionAttributeNames = {  "#id":"_id","#ame":"NAME1" },
        KeyConditionExpression = Key('_id').eq(id)
    )
    print(task)
    return render_template('newupdate.html',tasks = task)


@app.route('/delete' , methods = ['GET'])
def delete():
    id = request.values.get("_id")
    task = table.delete_item(
        Key={
            '_id':id
        }
    )
    print (task)
    return redirect('/')

@app.route( '/action' , methods = ['POST'] )
def action():
    id1 = request.values.get('_id')
    id = request.values.get('id')
    name = request.values.get('name')
    email = request.values.get('email')
    contactno = request.values.get('contactno')
    print (id)
    response = table.update_item(
        Key={
            '_id': id1,
        },
        UpdateExpression = " SET NAME1 = :n, EMAIL=:e, CONTACTNO=:c, ID=:i ",
        ExpressionAttributeValues={
            ':n':name,
            ':e':email,
            ':c':contactno,
            ':i':id            
        },
        ReturnValues="UPDATED_NEW"
    )
    print (response)
    return redirect('/')

@app.route('/newaddress' , methods = ['GET'])
def newaddress():
    id = request.values.get("_id")
    name5 = request.values.get("name5")
    task = table.query(
        ProjectionExpression = "#id , ID , #ame , EMAIL , CONTACTNO, ADDRESS ",
        ExpressionAttributeNames = { "#id":"_id","#ame":"NAME1" },
        KeyConditionExpression=Key('_id').eq(id)
    )
    print(task)
    return render_template('/addaddress.html' , _id = id , tasks = task ,name5 = name5 )

@app.route('/createAddress', methods = ['POST'] )
def createAddress():
    id1 = request.values.get("_id")
    select = request.values.get("select")
    line1 = request.values.get("line1")
    line2 = request.values.get("line2")
    contactno = request.values.get("contactno")
    print("------")
    print (id1,select,line1,line2,contactno)
    print("------")
    # print(request.args.get())
    
    if request.values.get("action1") == "Edit":
        print (select)
        response = table.update_item(
                Key={
                    '_id': id1,
                },
                UpdateExpression = "SET ADDRESS.#a = :l1",
                ExpressionAttributeNames={
                    '#a':select
                },
                ExpressionAttributeValues={                      
                    
                    ':l1':  [line1, line2, contactno]
                },
                ReturnValues="UPDATED_NEW"
            )      
    elif request.values.get("action1") == "Delete":
        print (select)
        response = table.update_item(
                Key={
                    '_id': id1,
                },
                UpdateExpression = "REMOVE ADDRESS.#as",
                ExpressionAttributeNames={
                    '#as': select
                },                              
                ReturnValues="ALL_NEW"
            )
    return redirect('/')
    # response1 = table.scan()
    # return render_template('test.html', data = response1)

@app.route('/deladdress',methods=['GET'])
def deladdress():
    print("teest")

@app.route('/')
def display():
    response = table.scan()
    return render_template('test.html', data = response)


if __name__ == '__main__':
    app.run(debug = True, host="192.168.43.140")
