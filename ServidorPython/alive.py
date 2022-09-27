from datetime import date, datetime
import email                
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
                bol = True if c.days < 1 and c.seconds < 70 else False

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
        time.sleep(5)

# EJEMPLO DE DICCIONARIOS

# dic_fHistorial = {
#     '_inte': float,
#     '_exte': float,
#     '_tipo': str,
#     '_out_0': int,
#     '_out_1': int,
#     '_contador': int,
#     '_date': datetime
#     }

# dic_Historial = {
#     'd_id': str,
#     '_name': str,
#     '_setpoint': float,
#     '_temperatura_interior': float,
#     '_temperatura_exterior': float,
#     '_out_0': int,
#     '_out_1': int,
#     '_histeresis_high': float,
#     '_histeresis_low': float,
#     '_temperatura_maxima': float,
#     '_date_maxima': date,
#     '_temperatura_minima': float,
#     '_date_minima': date,
#     '_date': date
#     }

# dic_Enterprises = {
#     'e_id': str,
#     'e_enterprise': str,
#     'e_password': str,
#     'e_phone': int,
#     'e_email': str,
#     'e_users':[
#         {
#             'u_id': str,
#             'u_name': str,
#             'u_password': str,
#             'u_phone': int,
#             'u_email': str,
#             'u_devices':[
#                 {
#                     'd_id': str,
#                     'd_name': str,
#                     'd_location': str,
#                     'd_setpoint': float,
#                     'd_histeresis_high': float,
#                     'd_histeresis_low': float,
#                     'd_online': bool,
#                     'd_grados': str,
#                     'd_alarma': float,
#                     'd_last_update': date
#                 },
#                 {
#                     'd_id': str,
#                     'd_name': str,
#                     'd_location': str,
#                     'd_setpoint': float,
#                     'd_histeresis_high': float,
#                     'd_histeresis_low': float,
#                     'd_online': bool,
#                     'd_grados': str,
#                     'd_alarma': float,
#                     'd_last_update': date
#                 }
#             ]
#         },
#         {
#             'u_id': str,
#             'u_name': str,
#             'u_password': str,
#             'u_phone': int,
#             'u_email': str,
#             'u_devices':[
#                 {
#                     'd_id': str,
#                     'd_name': str,
#                     'd_location': str,
#                     'd_setpoint': float,
#                     'd_histeresis_high': float,
#                     'd_histeresis_low': float,
#                     'd_online': bool,
#                     'd_grados': str,
#                     'd_alarma': float,
#                     'd_last_update': date
#                 }
#             ]
#         }
#     ]
# }
