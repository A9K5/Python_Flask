from flask_classy import FlaskView, route
import os
import boto3,json, csv
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
# from resource import config

s3 = boto3.resource('s3')
client = boto3.client('s3')


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['csv'])


class AWSS3(FlaskView):

    def index(self):
        return "API stuff"

    def allowed(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    @route('/upload/', methods=['GET', 'POST'])
    def upload_file(self):
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            if file and self.allowed(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                filepath = UPLOAD_FOLDER + filename
                s3.meta.client.upload_file(filepath, 'iotdash', filename)
                # return redirect(url_for('upload_file',filename=filename))
                return json.dumps({"Status": "OK"})
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

    @route('/listbucket/',methods=['GET'])
    def listbucket(self):
        # List bucket items---------------------------------
        msg = []
        finmsg = {}
        response = client.list_objects(Bucket='iotdash')
        for p in response['Contents']:
            msg.append(p['Key'])
        finmsg['Items'] = msg
        finmsg['Count'] = len(msg)
        return json.dumps(finmsg)

    @route('/parsecsv/',methods=['POST'])
    def parsecsv(self):
        # Download and parse file and return json-----------------------------------
        data = (request.data.decode('utf-8'))
        dataDict = json.loads(data)
        print (dataDict)
        filename = dataDict["filename"]
        filepath = UPLOAD_FOLDER + filename
        s3.meta.client.download_file('iotdash', filename, filepath)
        msg=[]
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                msg.append(row)
        return json.dumps({"Message":msg,"Filename":filename})


    @route('/jsoncsv/',methods=['POST'])
    def jsoncsv(self):
        data = (request.data.decode('utf-8'))
        dataDic = json.loads(data)
        dataDict = dataDic['Message']
        filename = dataDict['Filename']
        f = csv.writer(open("/tmp/json_csv.csv", "w+"))
        msg=[]
        for key in dataDict[0]:
            msg.append(key)
        # print (msg)
        f.writerow(msg)
        for p in dataDict: 
            s=[]
            for key in p:
                s.append(p[key])
            f.writerow(s)
        s3.meta.client.upload_file('/tmp/json_csv.csv', 'iotdash', filename)


        