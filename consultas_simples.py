from asyncio.windows_events import NULL
from datetime import datetime
from traceback import print_tb
from pymongo import MongoClient


client = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
# mongo = client.test

# print(client.list_database_names())
# sample_mflix = client['prueba_001']
# comme = sample_mflix['sub_prueba_001']
t = client['Tempec_Cloud']
e = t['Enterprises']

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

# documento = {
#     'e_id':'AA',
#     'name': 'Jessica Biel',
#     'sub':[
#         {
#             'u_id':'AAA',
#             'name': 'Gemma Arterton',
#             'subsub':[]
#         }
#     ]
# }

# dic = {
#     'e_id':'AA',
#     'name': 'Eva Green',
#     'users': [{
#         'u_id': 'AAA',
#         'u_name': 'Jesuca',
#         'device':[{
#             'd_id':'AAAA',
#             'd_name': 'Biel',
#         },
#         {
#             'd_id':'AAAB',
#             'd_name':'Jolie'
#         }
#         ],
#     }]
# }
# e.insert_one(dic)
dic = {
    'd_id':'a321',
    'd_name': 'JesususXD'
}

# e.update_one({'users.u_id':'ZZZ'}, {'$push' : {'users.u_id.devices' : dic }})
# e.update_one({'users.u_id': {'$all': ["ZZZ"]}},{'$push' : {'users' : dic }})

for r in e.aggregate([{'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", 'AAZ']}}}]):
    print(r['index'])
# query = e.aggregate([{'$unwind':'$users'},
#                         {'$match': {"users.u_id": {"$eq": 'ZZZ'}}}])

# for r in query:
#     print(r)
#     print("\n")



# for x in e.find({
#     '$and':[
#         {'e_id':'AA'},
#         {'users.u_id':'AAA'}
#     ]}):
#     print(x)

# for x in e.find({}):
#     print(x)
# mongo = MongoClient('127.0.0.1', 27017)
# db = mongo['Tempec']
# users = db['Users']
# historial = db['Historial']
# pruebas = db['pruebas']