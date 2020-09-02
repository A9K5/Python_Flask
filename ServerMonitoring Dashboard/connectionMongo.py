from pymongo import MongoClient

conn = MongoClient()
db = conn.iotdash4 #conn.name_of_db
# collection = db.users #db.table_name 