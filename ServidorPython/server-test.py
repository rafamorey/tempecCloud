#PROGRAMA DE PRUEBA PARA FILTRAR Y ALMACENAR DATOS

# librerias & cositas
from datetime import datetime
from turtle import goto                   
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      
from concurrent.futures import ThreadPoolExecutor    


def insertar_historial(opcion, msg_payload):
    print(opcion)
    if opcion != 'ack':
        print("No es AKNOLW")
        # consulta para obetenr datos faltantes   
        consult = users.aggregate([{"$unwind": "$devices"},
                                    {'$match': {"devices.d_id": {"$eq": msg_payload.split('/')[1]}}},
                                    {"$project": {'nombre':"$devices.name","setpoint":"$devices.setpoint","hish":"$devices.histeresis_high","hisl":"$devices.histeresis_low"}}])

        print("Pididendo los valores")
        # obteniendo valor de variables
        for x in consult:
            name = x['nombre']
            setp = x['setpoint']
            hish = x['hish']
            hisl = x['hisl']
        
        print("Obtube los valores")
        d_id = msg_payload.split('/')[1]
        _name = name
        _setpoint = setp
        _histeresis_high = hish
        _histeresis_low = hisl
        _out_0 = bool(int(msg_payload.split('/')[4]))
        _out_1 = bool(int(msg_payload.split('/')[5]))
        _temperatura_interior = float(msg_payload.split('/')[2])
        _temperatura_exterior = float(msg_payload.split('/')[3])
        print("Valores en variables")
        if opcion == '1st':
            print("Entre a primer")
            _temperatura_maxima = float(msg_payload.split('/')[2])
            _date_maxima = datetime.now()
            _temperatura_minima = float(msg_payload.split('/')[2])
            _date_minima = datetime.now()
            print("Sali de a primer")
        elif opcion == 'noack':
            print("Entre a noak")
            for g in historial.find({'d_id': d_id},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1}).sort('_date',-1).limit(1):
                #last_temperatura_interior = g['_temperatura_interior']
                #last_temperatura_exterior = g['_temperatura_exterior']
                last_temperatura_maxima = g['_temperatura_maxima']
                last_date_maxima = g['_date_maxima']
                last_temperatura_minima = g['_temperatura_minima']
                last_date_minima = g['_date_minima']
            
            print("Sali de noak")

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
        #historial.insert_one(dic)
        print("Se inserto el seguiente documento/diccionario en historial: ")
        print(dic)
        print("=======================================================================================================================================================")

def funcion_detectar_acknowlaged(msg_payload):
    d_id = msg_payload.split('/')[1]
    temperatura_interior = msg_payload.split('/')[2]
    #temperatura_exterior = msg_payload.split('/')[3]

    for g in historial.find({'d_id': d_id},{'_id':0,'_temperatura_interior':1, '_temperatura_exterior':1}).sort('_date',-1).limit(1):
        last_temperatura_interior = g['_temperatura_interior']
        #last_temperatura_exterior = g['_temperatura_exterior']

    if temperatura_interior > (last_temperatura_interior * 1.2) or temperatura_interior < (last_temperatura_interior * 0.8) :
        return 'ack', msg_payload
    else:
        return 'noack', msg_payload

def update_device(msg_payload):
    users.update_one({'devices._id': msg_payload.split('/')[1]},{'$set': {
                                            'devices.$.name' : msg_payload.split('/')[2],
                                            'devices.$.location' : msg_payload.split('/')[3],
                                             'devices.$.setpoint' : float(msg_payload.split('/')[4]),
                                             'devices.$.histeresis_high' : float(msg_payload.split('/')[5]), 
                                             'devices.$.histeresis_low': float(msg_payload.split('/')[6]) 
                                             }})
    print('Se actualizo la informacion')
    print("=======================================================================================================================================================")

# funcion principal
def main(msg_payload):   
    print("Main()")
    if users.count_documents({'users.devices.d_id':msg_payload.split('/')[1]}) > 0:            # ==> Saber si el dispositivo esta registrado
        print("Si Existo")
        if msg_payload.split('/')[0] == '10':
            print("Tipo 10")
            if historial.count_documents({'d_id':msg_payload.split('/')[1]}) <= 0:
                print("Primer msg")
                insertar_historial('1st', msg_payload)
            else:
                insertar_historial(funcion_detectar_acknowlaged(msg_payload))
                print("No primer msg")
        elif msg_payload.split('/')[0] == '20':
            print("Tipo 20")
            update_device(msg_payload)

# al conectarme al broker
def on_connect(client, userdata, flags,rc):
    client.subscribe("Tempec/Server")
    logo()

# al recivir un msg
def on_message(client, userdata, msg):
    print(msg.payload.decode())
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
# mongo = MongoClient('127.0.0.1', 27017)                                        #==> Aqui se crea un cliente y se conecta localmente a mongodb
mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                           #==> Uso la database Tempec que esta en mongogg
users = db['Enterprises']                                                      #==> Uso la coleccion Users que esta en la database Tempec
historial = db['Historial']                                                    #==> Uso la coleccion Historial que esta en la database Tempec
executor = ThreadPoolExecutor(max_workers=8)                                   #==> Determino la cantidad de treads que tendra mi thread'spool
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
