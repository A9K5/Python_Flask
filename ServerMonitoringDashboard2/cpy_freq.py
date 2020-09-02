import time
import datetime
import psutil
from pymongo import MongoClient

conn = MongoClient()
db = conn.iotdash5  # conn.name_of_db
collection = db.alluse  # db.table_name


t_end = time.time() + 60 * 15
while time.time() < t_end:
    p = psutil.Process()
    with p.oneshot():
        f1 = psutil.cpu_freq(percpu=True)[0][0]
        f2 = psutil.cpu_freq(percpu=True)[1][0]
        f3 = psutil.cpu_freq(percpu=True)[2][0]
        f4 = psutil.cpu_freq(percpu=True)[3][0]
        memtotal = psutil.virtual_memory().total/(1024 * 1024) # Values in mb.
        memused = psutil.virtual_memory().used/(1024 * 1024)
        disktotal =  psutil.disk_usage('/').total/(1024*1024*1024) # Value in Gb.
        diskused =  psutil.disk_usage('/').used/(1024*1024*1024)
    # Return CPU frequency as a nameduple including current, min and max frequencies expressed in Mhz
    try:
        collection.insert_one(
            {"freq1": f1, "freq2": f2, "freq3": f3, "freq4": f4, "time": time.time(),"memtotal":memtotal,"memused":memused,"disktotal":disktotal,"diskused":diskused})
        time.sleep(3)
        print(time.time(), f1, f2, f3, f4)
    except Exception as ex:
        print(ex)
