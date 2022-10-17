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

for z in enterprises.aggregate([{'$match': {'devices.id': {'$eq': 'AAAB'}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': 'AAAB'}}},
                            {'$project': {'_id':0, 'enterp':'$name', 'nombre': '$devices.name', 'sp': '$devices.setpoint', 'hmax': '$devices.hisH', 'hmin': '$devices.hisL'}}
                            ]):
    print(z)
    _name = z['nombre']
    _setpoint = z['sp']
    hisH = z['hmax']
    hisL  = z['hmin']