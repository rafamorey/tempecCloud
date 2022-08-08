#Consultas PyMongo
#AAA000 Devices
#000AAA Users

from datetime import datetime
# from unittest import result
from pymongo import MongoClient

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
#historial = db['Historial']

"""
Tempec
    Users
        id:super:admin:pass:phone:email:id_devices{}
    Devices
        id:name:location:setpoint:his_h:his_l:last_update
    Historial
        tipo:_id:temp_int:temp_ext:out_0:out_1
        id:name:setpoint:temp_ext:temp_int:out_0:out_1:his_h:his_l:temp_min:date_min:temp_max:date_max:last_update //In
"""

doc = {
    '_id':'AA01',
    'super': True,
    'name':'Eva Mendez',
    'password':'tiamomonzav',
    'phone': 6622902042,
    'email': 'eva@gmail.com',
    'devices': [
    {
        '_id': '00AD',
        'name': 'Fescocos',
        'location': 'Mexico, Sonora, Obregon, Caudillo',
        'setpoint': 18.0,
        'histeresis_high': 2.5,
        'histeresis_low': 1.0,
        'last_update': str(datetime.now())
    },
    {
        '_id': '00AE',
        'name': 'Congelame',
        'location': 'Mexico, Sonora, Obregon, Hipersona',
        'setpoint': 18.5,
        'histeresis_high': 1.0,
        'histeresis_low': 1.0,
        'last_update': str(datetime.now())
    }]
        }

users.insert_one(doc)

'''
doc = {
        '_id': '000AAB',
        '_super': '0',
        '_admin': 'Eva Mendez',
        '_pass': 'tiamo_monzav2',
        '_phone': 6622902042,
        '_email': 'emendez@gmail.com',
        'id_devices': ['AAA003'],
        'last_update': str(datetime.now())
        }
users.insert_one(doc)
'''

#col.delete_many({'Valor':{'$gt':'20'}})

#db.collection.find().sort({age:-1}).limit(1) // for MAX
#print(col.count_documents({}))

#query = users.find_one({'_id' : '000AAA'})
#nombre = str(query)
#print(nombre)


print(mongo.list_database_names())
print(db.list_collection_names())

#users.find({},{'_id':1})

'''
query={'x':1}
projection={'_id':0, '_admin':1} # show x but not show _id
users.find(query,projection)
'''
#results = users.find({})
#print([x['_admin'] for x in results])

results = users.find({'devices.name': {"$ne":'x'}},{'devices._id':1})
print([x for x in results])

#users.aggregate([{'$project' : {'_admin':'$_admin '}}])
#clientes.drop()

#users.delete_one({'_id':'000AAB'})
