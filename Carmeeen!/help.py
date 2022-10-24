from array import array
import datetime
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      
# import mejoras

# mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
mongo = MongoClient("mongodb+srv://rafaelDiinpec:Mr178910@tc.kshjevt.mongodb.net/?retryWrites=true&w=majority")

# db = mongo['Tempec_Cloud']     
db = mongo['test']                                            
enterprises = db['enterprises']                                            
historial = db['devices']  
f_historial = db['fHistorial_AAAB']
# f_historial = db['fHistorial_AAAZ']
# r = "fHistorial_AAAB"
# print(db.list_collection_names())

# for b in historial.find({'tempInt': {'$lt':15}}):
#     print(b['tempInt'])

# for n in historial.find({'id':'AAAB'},{'_id':0, 'id':1, 'tempInt':1, 'fake':1, 'contador':1, 'date':1}).sort('date',-1).limit(20):
#     print(n)
# print(historial.count_documents({'id':'AAAB'}))

# db[r].delete_many({'date': {'$lt':datetime.datetime.now()}})
# for t in historial.find({'id':'tempec1'}):
#     print(t)

for h in enterprises.find({'enterprise': 'DIINPEC'}):
    print(h)
    print("==>==>==>")
