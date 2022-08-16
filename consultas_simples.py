from asyncio.windows_events import NULL
from datetime import datetime
from pymongo import MongoClient

# Users
# AA00 ==> 00AA, 00AB, 00AC
# AA01 ==> 00AD, 00AE
# AA02 ==> 00AF, 00AG, 00AH
# AA03 ==> 00AI, 00AJ, 00AK, 00AL

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']
pruebas = db['pruebas']


#query = pruebas.find({})
#for r in query:
#    print(r)

print('=========================================================')

y = users.update_one({'devices._id':'00AA'},{'$set': {'devices.$.name' : 'Freezer', 'devices.$.setpoint': 22.2 } })
x = users.find({'devices._id': '00AA'})
for g in x:
    print(g)
#pruebas.delete_many({'_id': {'$ne':'AA08'}})
#pruebas.insert_one({'_id_h': '00AA', '_name': 'Freezer', '_setpoint': 18.0, '_temperatura_int': 20.81, '_temperatura_ext': 35.81, '_out_0': True, '_out_1': False, '_histeresis_high': 0.4, '_histeresis_low': 1.2, '_temperatura_maxima': 23.81, '_date_maxima': datetime.now(), '_temperatura_minima': 20.81, '_date_minima': datetime.now(), '_date': datetime.now()})