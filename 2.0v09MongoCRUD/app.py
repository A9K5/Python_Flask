from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

@app.route('/')
def index():
    
    #Database connection code goes here
    try:
        conn = MongoClient()
        print("Successfully connected .")
    except:
        print(" Could not connect to MongoDb.")
    
    #After connection rendering of page
    return render_template("dash.html")

@app.route('/create1')
def student():
    
    try:
        conn = MongoClient()
        print("Successfully connected .")
    except:
        print(" Could not connect to MongoDb.")
    
    db = conn.iotdash #conn.name_of_db
    collection = db.iotdash2
    rec_id1 = collection.insert_one( { 'x': 2 } ) 
    
    #print(" Could not create table .")
    print (rec_id1)
    return render_template("insert.html",result1 = rec_id1)
    #iotdash2 is the name of the table[collection] to be created

@app.route('/read')
def reader():
    
    ret = mongo.iotdash.iotdash2.find({})
    dict=[]
    for i in ret:
        dict.append(i)
    #print(cursor)
    return render_template("displayread.html",ret1=dict)


@app.route('/update')
def update():
    try:
        conn = MongoClient()
        print("Successfully connected .")
    except:
        print(" Could not connect to MongoDb.")
    try :
        db = conn.iotdash
        db.iotdash2.updateOne({ "x" : "1" },{ $set: { "x" : 3 } })
    except:
        print(e)
    return render_template("updatedisplay.html")



@app.route('/result',methods = ['POST','GET'] )
def result():
    if request.method == 'POST':
        try:
            conn = MongoClient()
            print("Successfully connected .")
        except:
            print(" Could not connect to MongoDb.")

        db = conn.database

        collection = db.iotdash
        emp_rec1 = {
        "name":"Mr.Geek",
        "position":"CTO",
        "domain":"delhi"
        }
        rec_id1 = collection.insert_one(emp_rec1)
        print (rec_id1)
        dict=[]
        for i in red_id1:
            dict.append(i)
        #result = request.form
        return render_template("result.html",result1 = dict)

if __name__ == '__main__':
    app.run(debug = True)