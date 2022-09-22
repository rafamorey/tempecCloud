from datetime import date, datetime                
from pymongo import MongoClient                                                      
import time                                      

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
users = db['Enterprises']                                            

def obtener_user(ux):
    for h in users.aggregate([{'$match': {'users.devices.d_id': ux}},
                        {'$unwind':'$users'},
                        {'$match':{'users.devices.d_id': ux}},
                        {'$project': {'users.u_id':1, '_id':0}}
                        ]):
        f = h['users']
    return str(f).split("'")[3]

def tic_tac():
    for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises' and r != 'devices_id':
            for g in db['fHistorial_'+ r.split('_')[1]].aggregate([{'$group': {'_id':{}, 'fecha': {'$last':'$_date'}}}]):
                c = datetime.now() - g['fecha']
                bol = True if c.days < 1 and c.seconds < 310 else False

                uu = obtener_user(r.split('_')[1])

                for j in users.aggregate([{'$match': {'users.u_id': uu}},
                            {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", uu]}}}]):
                    u = str(j['index'])

                for l in users.aggregate([{'$match': {'users.devices.d_id': r.split('_')[1]}},
                                    {'$unwind': '$users'},
                                    {'$match': {'users.u_id': uu}},
                                    {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.devices.d_id", r.split('_')[1]]}}}
                                    ]):
                    d = str(l['index'])

                users.update_one({'users.devices.d_id': str(r.split('_')[1])},{'$set': {
                                                f'users.{u}.devices.{d}.online' : bol,
                                                }})

def bucle():
    while True:
        tic_tac()
        print("Funcion Alive")
        time.sleep(5)

