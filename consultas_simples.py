from pymongo import MongoClient

client = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
# mongo = client.test

# sample_mflix = client['prueba_001']
# comme = sample_mflix['sub_prueba_001']
t = client['Tempec_Cloud']
e = t['Enterprises']
h = t['Historial']

# h.delete_many({'d_id': {'$eq':'AAAA'}})
e.update_one({'users.devices.d_id': 'AAAA'},{'$set': {
                                            f'users.0.devices.0.d_name' : 'GoKHAN',
                                        #  f'users.{u}.devices.{d}.location' : 'USA CALIFORNIA SACRAMENTO Las Cerdas',
                                            f'users.0.devices.0.setpoint' : 12.12,
                                            f'users.0.devices.0.histeresis_high' : 0.12, 
                                            f'users.0.devices.0.histeresis_low': 0.14}
                                            })
# documento = {
#     'e_id':'A0',
#     'enterprise':"Jolie Industries",
#     'e_password':'AyM<3',
#     'e_phone':6441767450,
#     'e_email':'a.jolie@gmail.com',
#     'users': [
#         {
#             'u_id':'0A',
#             'u_name':'Jesus Monzav',
#             'u_password':'cosita123',
#             'u_phone':6441767451,
#             'u_email':'rmonzav@gmail.com',
#             'devices': [
#                 {
#                     'd_id':'A000',
#                     'd_name':'Freezer',
#                     'location':'USA, California, Sacramento, Porki 1',
#                     'setpoint':18.0,
#                     'histeresis_high':1.5,
#                     'histeresis_low':0.5,
#                     'last_update':datetime.now()
#                 },
#                 {
#                     'd_id':'A001',
#                     'd_name':'Cooler',
#                     'location':'USA, California, Sacramento, Porki 2',
#                     'setpoint':16.0,
#                     'histeresis_high':1.0,
#                     'histeresis_low':1.0,
#                     'last_update':datetime.now()
#                 }
#             ]
#         },
#         {
#             'u_id':'0B',
#             'u_name':'Jorge Sentada',
#             'u_password':'cochiloco5',
#             'u_phone':6441767452,
#             'u_email':'jsent@gmail.com',
#             'devices': [
#                 {
#                     'd_id':'A002',
#                     'd_name':'MariFer',
#                     'location':'Mexico, Sonora, Obregon, Caudillo',
#                     'setpoint':18.0,
#                     'histeresis_high':1.5,
#                     'histeresis_low':0.5,
#                     'last_update':datetime.now()
#                 }
#             ]
#         }
#     ]
# }