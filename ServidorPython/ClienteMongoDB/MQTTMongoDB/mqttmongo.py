#Programa Para Almacenar Datos
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
devices = db['Devices']
historial = db['Historial']

def on_connect(client, userdata, flags,rc):
    client.subscribe("Tempec/#")
    print("Subscrito a Tempec y Contectado a Broker")

def on_message(client, userdata, msg):
    #10/AAA002/16.7/29.0/0/0
    #20/AAA001/16.0/0.5/0.5

    #id:name:setpoint:temp_ext:temp_int:out_0:out_1:his_h:his_l:temp_min:date_min:temp_max:date_max:update_server
    if str(devices.find_one({'_id': msg.payload.decode().split('/')[1]})) != "None":
        if msg.payload.decode().split('/')[0] == '10':
            print("10")
            doc = {
                '_id': msg.payload.decode().split('/')[1],
                '_temp_int': float(msg.payload.decode().split('/')[2]),
                '_temp_ext': float(msg.payload.decode().split('/')[3]),
                '_out_0': bool(msg.payload.decode().split('/')[4]),
                '_out_1': bool(msg.payload.decode().split('/')[5]),
                'update_server' : str(datetime.datetime.now())
                }
            print(doc)
        if msg.payload.decode().split('/')[0] == '20':
            print("20")

        #print(str(devices.find_one({'_id': msg.payload.decode().split('/')[0]})).split(',')[1].split(':')[1].split("'")[1])
    else:
        print("El dispositivo no con el _id = " + msg.payload.decode().split('/')[1] + " no existe.")

    '''
    doc = {
        'aux': d[0],
        'Granja': d[0]
    }
    '''
    #col.insert_one(doc)
    
    #print("Mensaje Insertado "  + msg.payload.decode() + " / " + str(datetime.datetime.now()))
    #print(str(datetime.date.today()))
    #print(str(datetime.datetime.now().hour))

monzav = mqtt.Client()
monzav.on_connect = on_connect
monzav.on_message = on_message
monzav.connect("test.mosquitto.org", 1883, 60)
#monzav.loop_start()
monzav.loop_forever()