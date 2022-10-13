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
f_historial = db['fHistorial_AAAB']
# f_historial = db['fHistorial_AAAZ']
     
inicio = datetime.datetime(2022, 10, 18, 1, 40, 47, 88000)    
# final = datetime.datetime(2022, 10, 13, 10, 30, 47, 88000)
# historial.delete_many({'d_id':'AAAB', 'date': {'$gt': final}})
v1_arr, v2_arr, k_arr = [],[],[]

# for g in db['fHistorial_AAAB'].find({},{'_id':0}).sort('date',-1).limit(5):
#     print(g['int'])
#     v1_arr.append(g['int'])
# print(v1_arr)

# for j in historial.find({'d_id':'AAAB', 'date': {'$gt':inicio}}):
#     print(j['tempInt'])

for x in historial.aggregate([
    {'$match': {'d_id': 'AAAB'}},
    #{'$match': {'date': {'$lt': inicio}}},#, '$lt': final}}},
    {'$project': {
        '_id':0, 
        'tempInt': '$tempInt',
        'contador': '$contador',
        'fake' : '$fake',
        'date': '$date'
        }}
        ]):
    xxx = str(x['contador']) + ' - ' + str(x['tempInt']) + ' - ' + str(x['fake']) + " - " + str(x['date'])
    print(xxx)
