from array import array
import datetime
from telnetlib import PRAGMA_HEARTBEAT
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      
# import mejoras

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")

db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['devices']  
f_historial = db['fHistorial_AAAB']
# f_historial = db['fHistorial_AAAZ']
r = "fHistorial_AAAB"

v1_arr, k_arr = [], []
v1_arr2, k_arr2 = [], []
# historial.delete_many({'date': {'$gt': datetime.datetime(2022, 10, 17, 10, 50, 0, 000000)}})

# for g in db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('date',-1).limit(5):
#     v1_arr.append(g['int'])
#     k_arr.append(g['grados'])
# print("Ultimos 5 de Fake Historial")
# print(v1_arr)
# print(k_arr)

for g in db['devices'].find({'d_id':'AAAB'},{'_id':0}).sort('date',-1).limit(10):
    print(f"In={g['tempInt']} fk= {g['fake']} \ndt= {g['date']}")

