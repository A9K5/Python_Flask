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

# dynamodb = boto3.resource('dynamodb')#, region_name='us-west-2', endpoint_url="http://localhost:8000")
# table = dynamodb.Table('IOT4')
# AllowedActions = ['both', 'publish', 'subscribe']

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/temp2')
def temp2():
    # startToken = request.values.get("startToken")
    # print(startToken)
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    tasks = 1
    startToken = 1
    response_iterator = paginator.paginate(
        TableName="IOT4",  
        # Limit=3
        PaginationConfig={
                'MaxItems': 5,
                'PageSize': 5,
                # 'StartingToken':startToken #page['LastEvaluatedKey']
            }      
    )
    for page in response_iterator:
        # print(page['Items'])
        # print(page)
        tasks = page['Items']
        # return (jsonify(page['Items']))
        for key in page:
            if key == "LastEvaluatedKey":
                print(page['LastEvaluatedKey']['_id']['S'])
                startToken = page['LastEvaluatedKey']['_id']['S']            
    return render_template('2paginator.html',startToken = startToken, tasks= tasks)
        # if page['LastEvaluatedKey'] != Null:
        #     startToken = page['LastEvaluatedKey']['_id']['S']
        #     print (startToken)
    
        # else:
        #     startToken = 0
        #     print(startToken)    
    
    # print(response_iterator)
    # return response_iterator

@app.route('/temp3',methods=['POST'])
def temp3():
    startToken = request.values.get("startToken")
    print(startToken)
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    tasks = 1
    # startToken = 1
    response_iterator = paginator.paginate(
        TableName="IOT4",  
        # Limit=3
        PaginationConfig={
            'MaxItems': 5,
            'PageSize': 5,
            'StartingToken': { '_id':'2018-06-26 15:09:51.103' } #page['LastEvaluatedKey']
        }      
    )
    print(response_iterator)
    for kay,val in response_iterator:
        print(kay)
    # for page in response_iterator:
    #     # print(page['Items'])
    #     # print(page)
        # tasks = page['Items']
        # return (jsonify(page['Items']))
        # for key in page:
    #         if key == "LastEvaluatedKey":
    #             print(page['LastEvaluatedKey']['_id']['S'])
    #             startToken = page['LastEvaluatedKey']['_id']['S']            
    # return (jsonify(startToken))
    # return render_template('2paginator.html',startToken = startToken, tasks= tasks)


@app.route('/temp4')
def temp4():
    # startToken = request.values.get("startToken")
    # print(startToken)
    client = boto3.client('dynamodb')
    paginator = client.get_paginator('scan')
    tasks = 1
    # startToken = 1
    response_iterator = paginator.paginate(
        TableName="IOT4",  
        # Limit=3
        PaginationConfig={
            'MaxItems': 5,
            'PageSize': 5            
        }      
    )
    for page in response_iterator:
        print(page)
    return("qwe")


if __name__ == '__main__':
    app.run(debug = True, host="192.168.0.117") # 192.168.43.140