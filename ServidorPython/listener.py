from datetime import date, datetime                
from pymongo import MongoClient                                                      
import time                                      

print("Iniciando MongoDB - " + str(datetime.now()))
mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
users = db['Enterprises']                                            
historial = db['Historial']      
devices_id = db['devices_id']
print("MongoDB Ejecutado - " + str(datetime.now()))    

def obtener_user(ux):
    for h in users.aggregate([{'$match': {'users.devices.d_id': ux}},
                        {'$unwind':'$users'},
                        {'$match':{'users.devices.d_id': ux}},
                        {'$project': {'users.u_id':1, '_id':0}}
                        ]):
        d = h['users']
    return str(d).split("'")[3]

def genesis():
    bol = False
    for h in devices_id.find({}):
        for g in historial.aggregate([{'$match': {'d_id': { '$eq':h['dev_id']}}},
                                        {'$group': {'_id':{}, 'fecha': {'$last':'$_date'}}}]):
            c = datetime.now() - g['fecha']
            if c.days < 1 and c.seconds < 30:
                print(h['dev_id'] + " ====")
                bol = True
            else:
                print(h['dev_id'] + " =")
                bol = False

            uu = obtener_user(h['dev_id'])

            for r in users.aggregate([{'$match': {'users.u_id': uu}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", uu]}}}]):
                u = str(r['index'])

            for l in users.aggregate([{'$match': {'users.devices.d_id': h['dev_id']}},
                                {'$unwind': '$users'},
                                {'$match': {'users.u_id': uu}},
                                {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.devices.d_id", h['dev_id']]}}}
                                ]):
                d = str(l['index'])

            users.update_one({'users.devices.d_id': str(h['dev_id'])},{'$set': {
                                            f'users.{u}.devices.{d}.online' : bol,
                                            }})

while True:
    print("><-><-><-><-><-><-><")
    genesis()
    time.sleep(5)

