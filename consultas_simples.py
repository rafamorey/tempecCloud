from pymongo import MongoClient

client = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
# mongo = client.test

# sample_mflix = client['prueba_001']
# comme = sample_mflix['sub_prueba_001']
t = client['Tempec_Cloud']
e = t['Enterprises']
h = t['Historial']
d = t['devices_id']

d.delete_many({'_id': {'$ne': 'AA'}})
