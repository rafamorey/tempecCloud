from array import array
import datetime
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      
# import mejoras

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")

db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['Historial']  
# f_historial = db['fHistorial_AAAA']
# f_historial = db['fHistorial_AAAZ']

# dic_f = {
#         'int': 26.6,
#         'ext': 32.5,
#         'grados': 'C',
#         'date': datetime.datetime.now()
#     }
# f_historial.insert_one(dic_f)

for r in db.list_collection_names():
    if r != 'Historial' and r != 'Enterprises':
        for x in enterprises.aggregate([{'$match': {'devices.id': {'$eq': r.split('_')[1]}}},
                        {'$unwind': '$devices'},
                        {'$match' : {'devices.id': {'$eq': r.split('_')[1]}}},
                        {'$project': {'_id':0,  'grados': '$devices.grados'}}
                        ]):
            grados = x['grados']
            print(grados)


# historial.delete_many({'d_id':'AAAZ'})
# db['fHistorial_AAAZ'].delete_many({'_inte': {'$gt': 0}})
# db['fHistorial_AAAZ'].delete_many({'_inte': -127})

