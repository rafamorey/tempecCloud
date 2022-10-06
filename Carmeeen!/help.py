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
                                
for x in enterprises.aggregate([{'$match': {'devices.name': {'$eq': 'Genesis'}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.name': {'$eq': 'Genesis'}}},
                            {'$project': {
                                'id': '$devices.id', 
                                'name': '$devices.name',
                                'setpoint': '$devices.setpoint',
                                'tempInt': '$devices.tempInt',
                                'tempExt': '$devices.tempExt',
                                'hisH': '$devices.hisH'
                                }}
                            ]):
    print(x)
# historial.delete_many({'d_id':'AAAZ'})
# db['fHistorial_AAAZ'].delete_many({'_inte': {'$gt': 0}})
# db['fHistorial_AAAZ'].delete_many({'_inte': -127})