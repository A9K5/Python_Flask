import time, datetime
import psutil
from pymongo import MongoClient

conn = MongoClient()
db = conn.iotdash4  # conn.name_of_db
collection = db.cpuusage  # db.table_name


t_end = time.time() + 60 * 15
while time.time() < t_end:

    #
    # ────────────────────────────────────────────── I ──────────
    #   :::::: C P U : :  :   :    :     :        :          :
    # ────────────────────────────────────────────────────────
    #

    
    
    cputime = psutil.cpu_percent()
    # Return a float representing the current system-wide CPU utilization as a percentage

    cpucount = psutil.cpu_count()
    # Return the number of logical CPUs in the system 

    cpucountlogical = psutil.cpu_count(logical=False)
    # Return the number of physical cores only (hyper thread CPUs are excluded) 

    cpuusable = len(psutil.Process().cpu_affinity())
    # The number of usable CPUs

    psutil.cpu_freq(percep=True)
    # Return CPU frequency as a nameduple including current, min and max frequencies expressed in Mhz

    #
    # ──────────────────────────────────────────────────── II ──────────
    #   :::::: M E M O R Y : :  :   :    :     :        :          :
    # ──────────────────────────────────────────────────────────────
    #
    mem = psutil.virtual_memory()
    # Return statistics about system memory usage as a named tuple

    #
    # ────────────────────────────────────────────────── III ──────────
    #   :::::: D I S K S : :  :   :    :     :        :          :
    # ────────────────────────────────────────────────────────────
    #

    diskpart = psutil.disk_partitions()
    # Return all mounted disk partitions as a list of named tuples

    #
    # ────────────────────────────────────────────────────── IV ──────────
    #   :::::: N E T W O R K : :  :   :    :     :        :          :
    # ────────────────────────────────────────────────────────────────
    #

    a = psutil.net_io_counters()
    # Return system-wide network I/O statistics as a named tuple

    b = psutil.net_connections()
    # Return system-wide socket connections as a list of named tuples. 

    c = psutil.net_if_addrs()
    # Return the addresses associated to each NIC (network interface card) 
    # installed on the system as a dictionary whose keys are the NIC names 
    # and value is a list of named tuples for each address assigned to the NIC.
    
    d = psutil.net_if_stats()
    # Return information about each NIC (network interface card) installed on the 
    # system as a dictionary whose keys are the NIC names and value is a named tuple 
    # with the following fields

    #
    # ──────────────────────────────────────────────────── V ──────────
    #   :::::: O T H E R S : :  :   :    :     :        :          :
    # ──────────────────────────────────────────────────────────────
    #

    boot_time =  datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    # Return the system boot time expressed in seconds since the epoch

    p = psutil.Process()
    with p.oneshot():
        p.name()
        p.cpu_times()
    # Utility context manager which considerably speeds up the retrieval of multiple process information
    #  at the same time. 

       
    try:
        collection.insert_one({"cpuusage": cputime,"time":time.time()})
        time.sleep(3)
        print(time.time(),cputime)
    except Exception as ex:
        print(ex)



#
# ────────────────────────────────────────────────────────────────────── VI ──────────
#   :::::: N U M B E R   O F   U S E R S : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────────
#

print (psutil.users())

#
# ────────────────────────────────────────────────────────────────────────────────── VII ──────────
#   :::::: P R O C E S S   L I S T   W I T H   P I D : :  :   :    :     :        :          :
# ────────────────────────────────────────────────────────────────────────────────────────────
#

for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
    print(proc.info)


#
# ──────────────────────────────────────────────────────────────────────── VIII ──────────
#   :::::: M O N G O D B   D E T A I L S : :  :   :    :     :        :          :
# ──────────────────────────────────────────────────────────────────────────────────
#


# Get server statistics

import os 
msg = {}
v = 'service mongod status > mongodstat.txt'
os.system(v)
f = open("mongodstat.txt","r")
fi = f.readlines()
for x in fi:
    if x.find('Active') > 0:
        msg['Active']=x[x.find('Active')+8:-1]
    elif x.find('Main PID') > 0:
        msg['Main PID']=x[x.find('Main PID')+10:-1]
    elif x.find('Tasks') > 0:
        msg['Tasks']=x[x.find('Tasks')+7:-1]
    elif x.find('Memory') > 0:
        msg['Memory']=x[x.find('Memory')+8:-1]    
    elif x.find('CPU') > 0:
        msg['CPU']=x[x.find('CPU')+5:-1] 
    elif x.find('CGroup') > 0:
        msg['CGroup']=x[x.find('CGroup')+8:-1] 
    elif x.find('Loaded') > 0:
        msg['Loaded']=x[x.find('Loaded')+8:-1]    

print(msg)


# Get user's

from pymongo import MongoClient
conn = MongoClient()
db = conn.iotdash4 
listing = db.command('usersInfo')
print(listing)
