#PROGRAMA DE PRUEBA PARA FILTRAR Y ALMACENAR DATOS

# librerias & cositas
from datetime import datetime
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import logging
import time
from concurrent.futures import ThreadPoolExecutor

# Saber si el dispositivo esta registrado
def if_exist(msg_device_id):
    if users.count_documents({'devices._id':msg_device_id}):
        return True
    else:
        return False

# Saber si es el primer MSG
def first_msg(msg_device_id):
    if historial.count_documents({'_id':msg_device_id}) <= 0:
        return True
    else:
        return False

# Insertar en Historial
def insertar_historial(opcion, msg_payload):

    if opcion != 'ack':
        # consulta para obetenr datos faltantes   
        consult = users.aggregate([{"$unwind": "$devices"},
                                    {'$match': {"devices._id": {"$eq": msg_payload.split('/')[1]}}},
                                    {"$project": {'nombre':"$devices.name","setpoint":"$devices.setpoint","hish":"$devices.histeresis_high","hisl":"$devices.histeresis_low"}}])

        # obteniendo valor de variables
        for x in consult:
            name = x['nombre']
            setp = x['setpoint']
            hish = x['hish']
            hisl = x['hisl']

        _id_d = msg_payload.split('/')[1]
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

        # No Primer Msg
        elif opcion == 'noack':
            for g in historial.find({'_id_h': _id_d},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1}).sort('_date',-1).limit(1):
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
            '_id_d': _id_d,
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
        #historial.insert_one(dic)
        print("Se inserto el seguiente documento/diccionario en historial: ")
        print(dic)
        print("=======================================================================================================================================================")

# Identificar acknowlaged
def funcion_detectar_acknowlaged(msg_payload):
    id_d = msg_payload.split('/')[1]
    temperatura_interior = msg_payload.split('/')[2]
    #temperatura_exterior = msg_payload.split('/')[3]

    for g in historial.find({'_id_h': id_d},{'_id':0,'_temperatura_interior':1, '_temperatura_exterior':1}).sort('_date',-1).limit(1):
        last_temperatura_interior = g['_temperatura_interior']
        #last_temperatura_exterior = g['_temperatura_exterior']

    if temperatura_interior > (last_temperatura_interior * 1.2) or temperatura_interior < (last_temperatura_interior * 0.8) :
        return 'ack', msg_payload
    else:
        return 'noack', msg_payload

# Actualizar datos del dispositivo
def update_device(msg_payload):
    users.update_one({'devices._id': msg_payload.split('/')[1]},{'$set': {
                                            'devices.$.name' : msg_payload.split('/')[2],
                                            'devices.$.location' : msg_payload.split('/')[3],
                                             'devices.$.setpoint' : float(msg_payload.split('/')[4]),
                                             'devices.$.histeresis_high' : float(msg_payload.split('/')[5]), 
                                             'devices.$.histeresis_low': float(msg_payload.split('/')[6]) 
                                             }})

# funcion principal
def main(msg_payload):   
    # -------------------------------------------------------------------------> saber si existe el dispositivo
    if if_exist(msg_payload.split('/')[1]):  
        # --------------------------------------------------------------> msg es de tipo 10
        if msg_payload.split('/')[0] == '10':
            # --------------------------------------------------> es el primer msg
            if first_msg(msg_payload.split('/')[1]):
                insertar_historial(1, msg_payload)
            # --------------------------------------------------> no es el primer msg
            else:
                insertar_historial(funcion_detectar_acknowlaged(msg_payload))
        # --------------------------------------------------------------> msg es de tipo 20
        elif msg_payload.split('/')[0] == '20':
            update_device(msg_payload)
        # --------------------------------------------------------------> msg es de tipo ??
        else:
            print('soy un ??')

# al conectarme al broker
def on_connect(client, userdata, flags,rc):
    client.subscribe("Tempec/Server")
    logo()

# al recivir un msg
def on_message(client, userdata, msg):
    executor.submit(main, msg.payload.decode())

# imprimir logo
def logo():
    print("TempecTempecTempec       TempecTempecTempec      TempecTempec      TempecTempec      TempecTempecTempec      TempecTempecTempec      TempecTempecTempec")
    time.sleep(0.2)
    print("      Tempec             Tempec                  Tempec   TempecTempec   Tempec      Tempec      Tempec      Tempec                  Tempec")
    time.sleep(0.2)
    print("      Tempec             TempecTempecTempec      Tempec      Tempec      Tempec      TempecTempecTempec      TempecTempecTempec      Tempec")
    time.sleep(0.2)
    print("      Tempec             Tempec                  Tempec                  Tempec      Tempec                  Tempec                  Tempec")
    time.sleep(0.2)
    print("      Tempec             TempecTempecTempec      Tempec                  Tempec      Tempec                  TempecTempecTempec      TempecTempecTempec")
    print("=======================================================================================================================================================")


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s') #==> Esto es para poder saber con que thread se ejecuto una tarea
mongo = MongoClient('127.0.0.1', 27017)                                        #==> Aqui se crea un cliente y se conecta localmente a mongodb
db = mongo['Tempec']                                                           #==> Uso la database Tempec que esta en mongodb
users = db['Users']                                                            #==> Uso la coleccion Users que esta en la database Tempec
historial = db['Historial']                                                    #==> Uso la coleccion Historial que esta en la database Tempec
executor = ThreadPoolExecutor(max_workers=8)                                   #==> Determino la cantidad de treads que tendra mi thread'spool
monzav = mqtt.Client()                                                         #==> Aqui creo un cliente mqtt
monzav.on_connect = on_connect                                                 #==> Cuando el cliente mqtt se conecte ejecutara la funcion on_connect
monzav.on_message = on_message                                                 #==> Cuando el cliente mqtt reciva un msg ejecutara la funcion on_message
monzav.connect("test.mosquitto.org", 1883, 60)                                 #==> Se conecta al broker de mosquitto
monzav.loop_forever()                                                          #==> Se inicia loop mqtt

# ====>            tipos de msg             <====
# 10/AAA002/16.7/29.0/0/0
# 20/AAA001/Nombre/Location/16.0/0.5/0.5
