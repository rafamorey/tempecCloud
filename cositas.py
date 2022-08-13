from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']

#col.delete_many({'Valor':{'$gt':'20'}})

#db.collection.find().sort({age:-1}).limit(1) // for MAX
#print(col.count_documents({}))
#print(historial.count_documents({}))
#query = users.find_one({'devices._id' : '00AA'})
'''
query = users.aggregate([{"$unwind": "$devices"},
                                {'$match': {"devices._id": {"$eq": '00AA'}}},
                                {"$project": {'nombre':"$devices.name","setpoint":"$devices.setpoint","hish":"$devices.histeresis_high","hisl":"$devices.histeresis_low"}}])
'''
# ==> query = users.find({'devices._id':'00AA'},{'_id':False, 'devices':{'$elemMatch':{'_id':'00AA'}}})
# ==> query = users.find({'devices._id':'00AA'},{'devices.$':True})
#query = users.count_documents({'devices._id': '00AA'})
#query = historial.count_documents({})
#print(query)
#print(type(query))
#query = users.find({})
#print([x for x in query])
#nombre = str(query)
#print(nombre)
#print(query['name'])
#print(query)

#print(mongo.list_database_names())
#print(db.list_collection_names())

#users.find({},{'_id':1})
#results = users.find({})
#print([x['_admin'] for x in results])

#results = users.find({'devices.name': {"$ne":'x'}},{'devices._id':1})
#print([x for x in results])

#users.aggregate([{'$project' : {'_admin':'$_admin '}}])
#clientes.drop()

#users.delete_one({'_id':'000AAB'})

'''
doc = {
    '_id':'AA02',
    'super': True,
    'name':'Jessie G',
    'password':'tiamomonzav',
    'phone': 6622902042,
    'email': 'jess@gmail.com',
    'devices': [
    {
        '_id': '00AF',
        'name': 'Freezer G',
        'location': 'USA, California, Sacramento, Jessie_Farm',
        'setpoint': 18.0,
        'histeresis_high': 0.5,
        'histeresis_low': 1.0,
        'last_update': str(datetime.now())
    },
    {
        '_id': '00AG',
        'name': 'JG',
        'location': 'USA, Californnia, Las Vegas, International Farm',
        'setpoint': 18.5,
        'histeresis_high': 0.2,
        'histeresis_low': 0.2,
        'last_update': str(datetime.now())
    }]
        }
'''