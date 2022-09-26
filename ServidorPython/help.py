from array import array
from datetime import date, datetime, timedelta
from operator import le
from re import A
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      


mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")

db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['Historial']  

for g in db['fHistorial_AAAB'].find({},{'_id':0}).sort('_date',-1).limit(5):
    pass
print(g['_valo'])