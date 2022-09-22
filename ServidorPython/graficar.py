from datetime import date, datetime                
from pymongo import MongoClient                                                      
import time                                      

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']     
historial = db['Historial']  

def grafica():
    for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            print(r.split('_')[1])
            for x in enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': 'AAAA'}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': 'AAAA'}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': 'AAAA'}}},
                            {'$project': {'_id':0,  'alive': '$users.devices.online'}}]):
                online = x['alive']
                if online:
                    v_arr = []
                    k_arr = []
                    for g in db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('_date',-1).limit(5):
                        v_arr.append(g['_valo'])
                        k_arr.append(g['_tipo'])
                    print(v_arr)
                    print(k_arr)
                else:
                    print("El equipo esta offline")

def bucle():
    while True:
        grafica()
        print("Graficar")
        time.sleep(60)