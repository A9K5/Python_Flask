from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId 
# from bson.code import Code

conn = MongoClient()
db = conn.iotdash #conn.name_of_db
collection = db.iotdash2 #db.table_name

app = Flask(__name__)

@app.route('/')
def index():   
    return render_template("dash.html")

@app.route('/create')
def create():
    return render_template("insert/newentry.html")

@app.route('/create1')
def student():

    id = request.args['id']
    name = request.args['name']
    city = request.args['city']
    
    rec_id1 = collection.insert_one({ "ID": int(id) ,"NAME": name ,"CITY": city }) 
    
    #print(" Could not create table .")
    print (rec_id1)
    return redirect('/')#render_template"insert.html",result1 = rec_id1)
    #iotdash2 is the name of the table[collection] to be created


@app.route('/read')
def reader():
    try:
        conn = MongoClient()
        print("Successfully connected .")
    except:
        print(" Could not connect to MongoDb.")
    db = conn.iotdash
    ret = db.iotdash2.find({})
    #dict=[]
    #for i in ret:
     #   dict.append(i)
      #  print(i)
    #print(cursor)
    return render_template("display/displayread.html",ret1s = ret )

@app.route('/newupdate' , methods = ['GET','POST'])
def newupdate():
    id = request.values.get("_id")
    task = collection.find({"_id":ObjectId(id)})
    return render_template('newupdate.html',tasks = task)

@app.route('/action', methods=['POST'])
def action():
    id1 = request.values.get("_id")
    name = request.values.get("name")
    id = request.values.get("id")
    city = request.values.get("city")
    collection.update({"_id":ObjectId(id1)} , {'$set':{"NAME":name , "ID":id , "CITY":city }})
    return redirect("/")

@app.route('/newdelete',methods=['GET'])
def newdelete():
    id1 = request.values.get("_id")
    collection.remove( {"_id":ObjectId(id1)} )
    return redirect("/")


@app.route('/update')
def update():
    return render_template("update.html")


@app.route('/Mongoupdate',methods=['GET','POST'])
def Mongoupdate():
    #if request.method == 'GET':
    oldxname = request.args['oldxname'] # request.values.get['oldname']
    newxname = request.args['newxname']
    print(oldxname,newxname)
    #oldxname = request.values.get("oldxname")
    #newxname = request.values.get("newxname")
    try:
        conn = MongoClient()
        print("Successfully connected .")
    except:
        print(" Could not connect to MongoDb.")
    try :
        db = conn.iotdash
        db.iotdash2.update({ "x" : int(oldxname) },{ '$set': { "x" : int(newxname) }})
    except:
        print("--->")
    return render_template("display/updatedisplay.html")
    

@app.route('/delete')
def delete():
    return render_template("delete.html")

@app.route('/Mongodelete',methods=['POST','GET'])
def Mongodelete():
    if request.method == 'POST':
        delname = request.form['delname']        
        collection.remove({ "x" : int(delname) })        
    return render_template("display/deletedisplay.html")
    




if __name__ == '__main__':
    app.run(debug = True)