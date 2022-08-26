#PROGRAMA DE PRUEBA PARA FILTRAR Y ALMACENAR DATOS

# librerias & cositas
from datetime import datetime                
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      
from concurrent.futures import ThreadPoolExecutor    


def insertar_historial(opcion, msg_payload):

    if opcion != 'ack':
        consult = users.aggregate([{'$match': {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0, 'nombre': '$users.devices.d_name', 'sp': '$users.devices.setpoint', 'hmax': '$users.devices.histeresis_high', 'hmin': '$users.devices.histeresis_low'}}])

        for x in consult:
            name = x['nombre']
            setp = x['sp']
            hish = x['hmax']
            hisl = x['hmin']

        d_id = msg_payload.split('/')[1]
        _name = name
        _setpoint = setp
        _histeresis_high = hish
        _histeresis_low = hisl
        _out_0 = bool(int(msg_payload.split('/')[4]))
        _out_1 = bool(int(msg_payload.split('/')[5]))
        _temperatura_interior = float(msg_payload.split('/')[2])
        _temperatura_exterior = float(msg_payload.split('/')[3])

        if opcion == '1st':
            _temperatura_maxima = float(msg_payload.split('/')[2])
            _date_maxima = datetime.now()
            _temperatura_minima = float(msg_payload.split('/')[2])
            _date_minima = datetime.now()

        elif opcion == 'noack':
            for g in historial.find({'d_id': d_id},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1}).sort('_date',-1).limit(1):
                #last_temperatura_interior = g['_temperatura_interior']
                #last_temperatura_exterior = g['_temperatura_exterior']
                last_temperatura_maxima = g['_temperatura_maxima']
                last_date_maxima = g['_date_maxima']
                last_temperatura_minima = g['_temperatura_minima']
                last_date_minima = g['_date_minima']

            if float(msg_payload.split('/')[2]) > last_temperatura_maxima:  
                _temperatura_maxima = float(msg_payload.split('/')[2])
                _date_maxima = datetime.now()
                _temperatura_minima = last_temperatura_minima
                _date_minima = last_date_minima

            elif float(msg_payload.split('/')[2]) < last_temperatura_minima:
                _temperatura_minima = float(msg_payload.split('/')[2])
                _date_minima = datetime.now()
                _temperatura_maxima = last_temperatura_maxima
                _date_maxima = last_date_maxima

            else:
                _temperatura_maxima = last_temperatura_maxima              
                _date_maxima = last_date_maxima
                _temperatura_minima = last_temperatura_minima
                _date_minima = last_date_minima

        dic = {
            'd_id': d_id,
            '_name': _name,
            '_setpoint': _setpoint,
            '_temperatura_interior': _temperatura_interior,
            '_temperatura_exterior': _temperatura_exterior,
            '_out_0': _out_0,
            '_out_1': _out_1,
            '_histeresis_high': _histeresis_high,
            '_histeresis_low': _histeresis_low,
            '_temperatura_maxima': _temperatura_maxima,
            '_date_maxima': _date_maxima,
            '_temperatura_minima': _temperatura_minima,
            '_date_minima': _date_minima,
            '_date': datetime.now()
        }
        historial.insert_one(dic)
        print(datetime.now())
        # print("=======================================================================================================================================================")

def funcion_detectar_acknowlaged(msg_payload):
    d_id = msg_payload.split('/')[1]
    temperatura_interior = float(msg_payload.split('/')[2])
    #temperatura_exterior = msg_payload.split('/')[3]

    for g in historial.find({'d_id': d_id},{'_id':0,'_temperatura_interior':1, '_temperatura_exterior':1}).sort('_date',-1).limit(1):
        last_temperatura_interior = g['_temperatura_interior']
        #last_temperatura_exterior = g['_temperatura_exterior']

    if temperatura_interior > (last_temperatura_interior * 1.5) or temperatura_interior < (last_temperatura_interior * 0.5):
        return "ack"
    else:
        return "noack"

def obtener_user(ux):
    for h in users.aggregate([{'$match': {'users.devices.d_id': ux}},
                        {'$unwind':'$users'},
                        {'$match':{'users.devices.d_id': ux}},
                        {'$project': {'users.u_id':1, '_id':0}}
                        ]):
        d = h['users']
    return str(d).split("'")[3]

def update_device(msg_payload):
    print(msg_payload.split('/')[1])
    dd = msg_payload.split('/')[1]
    uu = obtener_user(dd)
    for r in users.aggregate([{'$match': {'users.u_id': uu}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", uu]}}}]):
        u = str(r['index'])

    for h in users.aggregate([{'$match': {'users.devices.d_id': dd}},
                        {'$unwind': '$users'},
                        {'$match': {'users.u_id': uu}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.devices.d_id", dd]}}}
                        ]):
        d = str(h['index'])
    print("u: " + str(u) + "d: " + str(d) + "user: " + str(uu) + "devices: " + str(dd))
    users.update_one({'users.devices.d_id': dd},{'$set': {
                                             f'users.{u}.devices.{d}.d_name' : msg_payload.split('/')[2],
                                            #  f'users.{u}.devices.{d}.location' : 'USA CALIFORNIA SACRAMENTO Las Cerdas',
                                             f'users.{u}.devices.{d}.setpoint' : float(msg_payload.split('/')[4]),
                                             f'users.{u}.devices.{d}.histeresis_high' : float(msg_payload.split('/')[5]), 
                                             f'users.{u}.devices.{d}.histeresis_low': float(msg_payload.split('/')[6])
                                             }})

    print('Se actualizo la informacion')
    print("=======================================================================================================================================================")

def main(msg_payload):   
    if users.count_documents({'users.devices.d_id':msg_payload.split('/')[1]}) > 0:
        if msg_payload.split('/')[0] == '10':
            if historial.count_documents({'d_id':msg_payload.split('/')[1]}) <= 0:
                insertar_historial('1st', msg_payload)
            else:
                insertar_historial(funcion_detectar_acknowlaged(msg_payload), msg_payload)
        elif msg_payload.split('/')[0] == '20':
            print("Tipo 20")
            update_device(msg_payload)
    else:
        print("Do babes")

# al conectarme al broker
def on_connect(client, userdata, flags,rc):
    client.subscribe("Tempec/Server")
    logo()

# al recivir un msg
def on_message(client, userdata, msg):
    executor.submit(main, msg.payload.decode())

# imprimir logo
def logo():
    print("               TempecTempecTempec       TempecTempecTempec      TempecTempec      TempecTempec      TempecTempecTempec      TempecTempecTempec      TempecTempecTempec")
    time.sleep(0.2)
    print("                     Tempec             Tempec                  Tempec   TempecTempec   Tempec      Tempec      Tempec      Tempec                  Tempec")
    time.sleep(0.2)
    print("                     Tempec             TempecTempecTempec      Tempec      Tempec      Tempec      TempecTempecTempec      TempecTempecTempec      Tempec")
    time.sleep(0.2)
    print("                     Tempec             Tempec                  Tempec                  Tempec      Tempec                  Tempec                  Tempec")
    time.sleep(0.2)
    print("                     Tempec             TempecTempecTempec      Tempec                  Tempec      Tempec                  TempecTempecTempec      TempecTempecTempec")
    print("=======================================================================================================================================================")


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s') #==> Esto es para poder saber con que thread se ejecuto una tarea
# mongo = MongoClient('127.0.0.1', 27017)                                        #==> Aqui se crea un cliente y se conecta localmente a mongodb
mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                           #==> Uso la database Tempec que esta en mongogg
users = db['Enterprises']                                                      #==> Uso la coleccion Users que esta en la database Tempec
historial = db['Historial']                                                    #==> Uso la coleccion Historial que esta en la database Tempec
executor = ThreadPoolExecutor(max_workers=10)                                  #==> Determino la cantidad de treads que tendra mi thread'spool
monzav = mqtt.Client()                                                         #==> Aqui creo un cliente mqtt
monzav.on_connect = on_connect                                                 #==> Cuando el cliente mqtt se conecte ejecutara la funcion on_connect
monzav.on_message = on_message                                                 #==> Cuando el cliente mqtt reciva un msg ejecutara la funcion on_message
monzav.connect("test.mosquitto.org", 1883, 60)                                #==> Se conecta al broker de mosquitto
#monzav.connect("6c665d3e9b974b849cffc4266267b47b.s2.eu.hivemq.cloud", 8883, 10)
monzav.loop_forever()                                                          #==> Se inicia loop mqtt

# ====>            tipos de msg             <====
# Tipo/ID/TempInterior/TempExterior/Out0/Out1
# 10/AAAA/16.7/29.0/0/0
#
# Tipo/ID/Nombre/Ubicacion/Setpoint/Hist+/Hist-
# 20/AAA001/Freezer/Obregon Caudillo/16.0/0.5/0.5
