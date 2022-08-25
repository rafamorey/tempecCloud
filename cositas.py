from asyncio.windows_events import NULL
from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']
pruebas = db['pruebas']

# https://www.codehoven.com/mongodb-aggregate-operaciones-agregacion-pipeline/
# ==> Obtener datos (especificos) de un subdocumento
query = users.aggregate([{"$unwind": "$devices"},
                                {'$match': {"devices._id": {"$eq": '00AA'}}},
                                {"$project": {'nombre':"$devices.name","setpoint":"$devices.setpoint","hish":"$devices.histeresis_high","hisl":"$devices.histeresis_low"}}])
for r in query:
    print(r)
# ||
query = users.find({'devices._id':'00AA'},{'_id':False, 'devices':{'$elemMatch':{'_id':'00AA'}}})
for r in query:
    print(r)
# ||
query = users.find({'devices._id':'00AA'},{'devices.$':True})
for r in query:
    print(r)

# ==> Obtener el indix de un array
for r in pruebas.aggregate([{
    '$project':{
        '_id':0, 
        'index': {
            '$indexOfArray': ["$users.u_id", 'AAZ']
            }
            }
            }]):
    print(r['index'])

# ==> Agregar subdocumento a documento
pruebas.update_one({'_id': 'AA05'}, {'$push' : {'devices' : {'_id':'AA0H', 'name':'Moam'}}})

# ==> Obtener el valor maximo/minimo
a = users.aggregate([{
    '$group': {'_id': 'AA00', 'max': {'$max': '$phone'}}
}])
for g in a:
    print(g)
# ||
x = pruebas.find({'_id_h':'00AA'},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1}).sort('_date',-1).limit(1)
for g in x:
    print(g)
# ||
x = pruebas.aggregate([
    {'$match': {'_id_h': '00AA'}},
    {'$group': {'_id': 'skere','max': {'$max': '$_date'}}}
    ])
for g in x:
    print(g)
# ||
x = pruebas.aggregate([{'$match': {'_id_h': '00AA'}},
                    {'$project' : {'_id':0}},{'$sort' : {'_date' : -1}},{'$limit' : 1}])
for g in x:
    print(g)
    
# ==> Actualizar datos de un subdocumento
users.update_one({'devices._id': 'AA00'},{'$set': {
                                        'devices.$.name' : 'Wanda',
                                        'devices.$.location' : 'Mi corazon',
                                         'devices.$.setpoint' : 16.0,
                                         'devices.$.histeresis_high' : 2.0, 
                                         'devices.$.histeresis_low': 0.7 
                                         }})
                                         
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

# ==> Para obtener los estudiantes de nombre “Juan”
pruebas.aggregate([{'$match' : {'nombre' : 'Juan'}}])

# ==> Si queremos solo ver el nombre de los estudiantes registrados:
pruebas.aggregate([{'$project' : {'nombre':1, '_id':0}}])

# ==> Para mostrar el apellido como “segundoNombre” lo haríamos de la siguiente forma:
pruebas.aggregate([{'$project' : {'nombre':1, '_id':0, 'segundoNombre':"$nombre"}}])

# ==> Si quisiéramos obtener el nombre y apellido del estudiante:
pruebas.aggregate([{'$project' : {'_id':0, 'nombreCompleto' : {'$concat' : ["$nombre"," ","$apellido"]}}}])
# ==> Si queremos obtener los estudiantes ordenados según su edad de forma ascendente:
pruebas.aggregate([{'$project' : {'nombre':1,'edad':1,'_id':0}},{'$sort' : {'edad' : 1}}])
# ==> Si queremos obtener solo 3 estudiantes más jóvenes:
pruebas.aggregate([{'$project' : {'nombre':1,'edad':1,'_id':0}},{'$sort' : {'edad' : 1}},{'$limit' : 3}])
# ==> Si queremos obtener los 3 estudiantes más jóvenes luego de los primeros 2:
pruebas.aggregate([{'$project' : {'nombre':1,'edad':1,'_id':0}},{'$sort' : {'edad' : 1}},{'$skip':2},{'$limit' : 3}])
# ==> Si queremos obtener la cantidad de estudiantes menores a 20 años:
pruebas.aggregate([{'$match' : {'edad' : { '$lt' : 20}}}, {'$count' : "Estudiantes menores a 20 años"}])
# ==> Si deseamos agrupar los estudiantes separando los mayores de edad de los menores de edad:
pruebas.aggregate([{'$group' : { '_id' : {'$lt' : ['$edad',18]}, 'edades' : {'$push' : {'edad' : '$edad'}}}}])
# ==> Si queremos agrupar los estudiantes por el programa que cursan:
pruebas.aggregate([{'$group' : { '_id ': '$programa', 'count' : {'$sum' : 1}}}])

# print(e.count_documents({
#     '$and':[
#         {'e_id':'AA'},
#         {'users.u_id':'AAA'}
#     ]
# }))
# ==> Operadores en MongoDB
# $ne  !=
# $eq  ==
# $lt  <
# $lte <=
# $gt  >
# $gte >=
# $in  dentro de
# $nin !dentro de
# 
# | | | | | | | | | | | SAMPLES | | | | | | | | | | | | 
# 
# db.libros.find( { editorial: { $nin : ['Planeta'] } })
# db.libros.find( { editorial: { $in : ['Planeta'] } })
# db.libros.find( { precio: { $gte : 20 , $lte : 45} })
# db.libros.find( { cantidad: { $ne : 50 }})
# db.libros.find( { cantidad: { $gte : 50 }})
# db.libros.find({ precio: { $gt:40 }})

# Modelo para coleccion 'users'

documento = {
    'e_id':'A0',
    'enterprise':"Jolie Industries",
    'e_password':'AyM<3',
    'e_phone':6441767450,
    'e_email':'a.jolie@gmail.com',
    'users': [
        {
            'u_id':'0A',
            'u_name':'Jesus Monzav',
            'u_password':'cosita123',
            'u_phone':6441767451,
            'u_email':'rmonzav@gmail.com',
            'devices': [
                {
                    'd_id':'A000',
                    'd_name':'Freezer',
                    'location':'USA, California, Sacramento, Porki 1',
                    'setpoint':18.0,
                    'histeresis_high':1.5,
                    'histeresis_low':0.5,
                    'last_update':datetime.now()
                },
                {
                    'd_id':'A001',
                    'd_name':'Cooler',
                    'location':'USA, California, Sacramento, Porki 2',
                    'setpoint':16.0,
                    'histeresis_high':1.0,
                    'histeresis_low':1.0,
                    'last_update':datetime.now()
                }
            ]
        },
        {
            'u_id':'0B',
            'u_name':'Jorge Sentada',
            'u_password':'cochiloco5',
            'u_phone':6441767452,
            'u_email':'jsent@gmail.com',
            'devices': [
                {
                    'd_id':'A002',
                    'd_name':'MariFer',
                    'location':'Mexico, Sonora, Obregon, Caudillo',
                    'setpoint':18.0,
                    'histeresis_high':1.5,
                    'histeresis_low':0.5,
                    'last_update':datetime.now()
                }
            ]
        }
    ]
}

# db.getCollection("students").aggregate([
#     {$unwind:"$scores"},
#     {$group: { _id: "$name", promedio: {$avg: "$scores.score"}}}
# ])

# db.getCollection("students").aggregate([
#     {$unwind:"$scores"},
#     {$match: {"scores.type":{$ne:"quiz"}}},
#     {$group: { _id: "$name", promedio_no_quiz: {$avg: "$scores.score"}}}
# ])

# db.getCollection("students").aggregate([
#     {$unwind:"$scores"},
#     {$match: {"scores.type":{$eq:"exam"}}},
#     {$project:{scorr:"$scores.score"}},
#     {$group:{_id:{},Promedio_Global:{$avg:"$scorr"}}}
# ])

# function mapeame()
# {
#     var k = this.name;
    
#     for(var x = 0; x < this.scores.length; x++)
#     {
#         var v = this.scores[x].score;
#         emit(k, v);
#     }
# }

# function lo_otro(k, v)
# {
#     var prom = Array.sum(v)/v.length
#     return prom
# }

# db.getCollection("students").mapReduce
# (
#     mapeame,
#     lo_otro,
#     {out:{merge:"prom"}}
# )