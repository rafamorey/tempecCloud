from datetime import datetime
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
# import paho.mqtt.publish as publish                         
import time                                      
from concurrent.futures import ThreadPoolExecutor
import alive
import graficar

def insertar_f_historial(msg_payload : str):
    for x in enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0,  'tipo': '$users.devices.grados'}}]):
           
        tipo = x['tipo']

    f_historial = db['fHistorial_' + str(msg_payload.split('/')[1])]

    dic_f = {
        '_valo': float(msg_payload.split('/')[2]),
        '_tipo': tipo,
        '_date': datetime.now()
    }
    f_historial.insert_one(dic_f)

def obtener_user(ux):
    for h in enterprises.aggregate([{'$match': {'users.devices.d_id': ux}},
                        {'$unwind':'$users'},
                        {'$match':{'users.devices.d_id': ux}},
                        {'$project': {'users.u_id':1, '_id':0}}
                        ]):
        f = h['users']
    return str(f).split("'")[3]

def update_device(msg_payload):
    dd = msg_payload.split('/')[1]
    uu = obtener_user(dd)
    for r in enterprises.aggregate([{'$match': {'users.u_id': uu}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", uu]}}}]):
        u = str(r['index'])

    for h in enterprises.aggregate([{'$match': {'users.devices.d_id': dd}},
                        {'$unwind': '$users'},
                        {'$match': {'users.u_id': uu}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.devices.d_id", dd]}}}
                        ]):
        d = str(h['index'])
 
    enterprises.update_one({'users.devices.d_id': dd},{'$set': {
                                             f'users.{u}.devices.{d}.d_name' : msg_payload.split('/')[2],
                                            #  f'users.{u}.devices.{d}.location' : 'USA CALIFORNIA SACRAMENTO Las Cerdas',
                                             f'users.{u}.devices.{d}.setpoint' : float(msg_payload.split('/')[3]),
                                             f'users.{u}.devices.{d}.histeresis_high' : float(msg_payload.split('/')[4]), 
                                             f'users.{u}.devices.{d}.histeresis_low': float(msg_payload.split('/')[5]),
                                             f'users.{u}.devices.{d}.grados': float(msg_payload.split('/')[6]),
                                             f'users.{u}.devices.{d}.alarma': float(msg_payload.split('/')[7]),
                                             f'users.{u}.devices.{d}.last_update' : datetime.now()
                                             }})

    print("====Update==================================" + str(datetime.now()) +"=============================================")

def main(msg_payload):   
    print(msg_payload)
    if enterprises.count_documents({'users.devices.d_id':msg_payload.split('/')[1]}) > 0:
        if msg_payload.split('/')[0] == '10':
            insertar_f_historial(msg_payload)
        elif msg_payload.split('/')[0] == '20':
            update_device(msg_payload)

def on_connect(client, userdata, flags, rc):
    client.subscribe("Tempec/Server")
    print("Ready")
    print("      for")
    print("          Duty")

def on_message(client, userdata, msg):
    executor.submit(main, msg.payload.decode())

executor = ThreadPoolExecutor(max_workers=10)           

try:        
    print("Iniciando MongoDB...")
    mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
    db = mongo['Tempec_Cloud']                                                   
    enterprises = db['Enterprises']                                            
    historial = db['Historial']            
    print("MongoDB iniciado")                                  
except:
    print("No se pudo establecer conexion con MongoDB")   
    
try:
    print("Iniciando MQTT...")
    monzav = mqtt.Client()  
    monzav.connect("test.mosquitto.org", 1883, 60) 
    print("MQTT Iniciando")
    monzav.on_connect = on_connect                                     
    monzav.on_message = on_message                                                 
    #monzav.connect("6c665d3e9b974b849cffc4266267b47b.s2.eu.hivemq.cloud", 8883, 10)
    executor.submit(graficar.bucle)
    executor.submit(alive.bucle)
    monzav.loop_forever()    
except:
    print("No se pudo establecer conexion con Mosquitto")

