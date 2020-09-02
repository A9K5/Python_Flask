from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

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
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    # print(dataDict)
    id = dataDict['id']
    name = dataDict['name']
    email = dataDict['email']
    contactno = dataDict['contactno']

    
    response = table.query(
        IndexName='EMAIL-index',
        KeyConditionExpression=Key('EMAIL').eq(email)
    )

    print(response)
    if(response['Count'] == 0):
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
        if (response['ResponseMetadata']['HTTPStatusCode']   == 200 ):
            return(jsonify({'status': 'User created successfully!'})), 201
        else:
            return(jsonify({'status': 'User not created!'})), 403
    else:
        return(jsonify({'status': 'User already exists!'})), 403

@app.route('/delete' , methods = ['POST'])
def delete():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    email = dataDict["email"]
    response = table.query(
        IndexName='EMAIL-index',
        KeyConditionExpression=Key('EMAIL').eq(email)
    )
    if(response['Count'] == 1):
        response1 = table.delete_item(
                Key={
                    '_id': response['Items'][0]["_id"],
                }
            ) 
        return(jsonify({'status': 'user deleted successfully'})), 201
    else:
        return(jsonify({'status': 'Email ID does not exists!'})), 403

   
@app.route('/createAddress', methods = ['POST'] )
def createAddress():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    email = dataDict["email"]
    select = dataDict["select"]
    line1 = dataDict["line1"]
    line2 = dataDict["line2"]
    contactno = dataDict["contactno"]

    response = table.query(
        IndexName='EMAIL-index',
        KeyConditionExpression=Key('EMAIL').eq(email)
    )
    if(response['Count'] == 1):
        response1 = table.update_item(
                Key={
                    '_id': response['Items'][0]["_id"],
                },
                UpdateExpression = "SET ADDRESS.#a = :l1",
                ExpressionAttributeNames={
                    '#a':select
                },
                ExpressionAttributeValues={                      
                    
                    ':l1':  [line1, line2, contactno]
                },
                ReturnValues="ALL_NEW"
            ) 
        return(jsonify({'status': 'Address updated successfully'})), 201
    else:
        return(jsonify({'status': 'Email ID does not exists!'})), 403

@app.route('/deleteAddress', methods = ['POST'] )
def deleteAddress():
    data = (request.data.decode('utf-8'))
    dataDict = json.loads(data)
    email = dataDict["email"]
    select = dataDict["select"]
    response = table.query(
        IndexName='EMAIL-index',
        KeyConditionExpression=Key('EMAIL').eq(email)
    )
    if(response['Count'] == 1):
        if select in response['Items'][0]['ADDRESS']:
            response1 = table.update_item(
                    Key={
                        '_id': response['Items'][0]["_id"],
                    },
                    UpdateExpression = "REMOVE ADDRESS.#as",
                    ExpressionAttributeNames={
                       '#as': select
                    },                              
                    ReturnValues="ALL_NEW"
                )
            return(jsonify({'status': 'Address deleted successfully'})), 201
        else:
            return(jsonify({'status':"Address does not exist."}))
    else:
        return(jsonify({'status': 'Email ID does not exists!'})), 403

@app.route('/')
def display():
    response = table.scan()
    #     ExclusiveStartKey={
    #         '_id': '2018-06-26 13:39:27.027'
    #     },
    #     Limit=2
    # )
    print(response)
    return ("response")

    # return jsonify({'userList': response['Items']})

@app.route('/temp')
def index12():
    response = table.scan()
    print(response)
    return render_template('2testjquery.html', tasks=response['Items'])
    # search = False
    # q = request.args.get('q')
    # if q:
    #     search = True

    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # response = table.scan()
    # pagination = Pagination(page=page, total=response.count(), search=search, record_name='response')
    # return render_template('display/index.html',users=response, pagination=pagination,)

@app.route('/temp2')
def temp2():
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    response_iterator = paginator.paginate(
        TableName="IOT4",        
    )
    for page in response_iterator:
        print(page)
        return (page)
    return("null")
    # print(response_iterator)
    # return response_iterator


if __name__ == '__main__':
    app.run(debug = True, host="192.168.43.140")
