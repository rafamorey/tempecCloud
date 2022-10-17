import pymongo    

print("Iniciando MongoDB")
mongo = pymongo.MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['Historial']            
print("MongoDB iniciado")

historial.rename("devices")

print(db.list_collection_names())