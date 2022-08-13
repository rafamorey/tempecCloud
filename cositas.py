from asyncio.windows_events import NULL
from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']
pruebas = db['pruebas']


#db.collection.find().sort({age:-1}).limit(1) // for MAX
#print(col.count_documents({}))
#print(historial.count_documents({}))
#query = users.find_one({'devices._id' : '00AA'})
doc = {
    '_id':'AA05',
    'super': True,
    'name':'Jessica Biel',
    'password':'tiamomonzav',
    'phone': 6622902042,
    'email': 'biel@gmail.com',
    'devices': []
        }
#pruebas.insert_one(doc)
#x = pruebas.find_one({'_id':'AA05'})
'''
query = users.aggregate([{"$unwind": "$devices"},
                                {'$match': {"devices._id": {"$eq": '00AA'}}},
                                {"$project": {'nombre':"$devices.name","setpoint":"$devices.setpoint","hish":"$devices.histeresis_high","hisl":"$devices.histeresis_low"}}])
'''
# ==> query = users.find({'devices._id':'00AA'},{'_id':False, 'devices':{'$elemMatch':{'_id':'00AA'}}})
# ==> query = users.find({'devices._id':'00AA'},{'devices.$':True})
#pruebas.find({'_id':'AA05'},{'devices.$':True})

# ==> Obtener subdocumentos de documento
users.find({'devices._id':'00AA'},{'_id':False, 'devices':{'$elemMatch':{'_id':'00AA'}}})

# ==> Agregar subdocumento a documento
pruebas.update_one({'_id': 'AA05'}, {'$push' : {'devices' : {'_id':'AA0H', 'name':'Moam'}}})

# ==> Obtener el valor maximo/minimo
a = users.aggregate([{
    '$group': {'_id': 'AA00', 'max': {'$max': '$phone'}}
}])
for g in a:
    print(g)

# ==> Borrar el primer documento con id
pruebas.delete_one({'_id': 'AA06'})

# ==> Borrar una coleccion
pruebas.drop()

# ==> Borrar todo donde phone > 20
users.delete_many({'phone':{'$gt':'20'}})

# ==> Obtener cuenta de docuemtnos con filtro
users.count_documents({'_id': '00AA'})

# ==> Obteener cuenta de documentos sin filtro
historial.count_documents({})

# ==> Obtener todo
users.find({})

# ==> Obtener lista de db
print(mongo.list_database_names())

# ==> Obtener lista de colecciones
print(db.list_collection_names())

# ==> Obtener todos y solo los _id
results = users.find({},{'_id':1})
print([x for x in results])
# ||
results = users.find({})
print([x['_admin'] for x in results])
# ||
results = users.find({'devices.name': {"$ne":'x'}},{'devices._id':1})
print([x for x in results])

# Modelo para coleccion 'users'
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