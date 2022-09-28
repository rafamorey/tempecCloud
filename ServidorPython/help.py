from array import array
import datetime
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      


mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")

db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['Historial']  

historial.delete_many({'d_id':'AAAA'})
db['fHistorial_AAAA'].delete_many({'_inte': {'$gt': 0}})
db['fHistorial_AAAA'].delete_many({'_inte': -127})

