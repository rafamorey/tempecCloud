#Programa Para Almacenar Datos
from datetime import datetime
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']

def saber_si_existe(wanda):
    if str(users.find_one({'devices._id': wanda.split('/')[1]})['name']) != "None":
        return True
    else:
        return False
    
    
def somebody_save_me(msg_payload, msg_topic):   
    if saber_si_existe(msg_payload):  
        '''    
        if msg_payload.split('/')[0] == '10':
            print("El tipo de mensaje es 10 y sé que hacer")
            doc = {
                '_id': msg_payload.split('/')[1],
                '_temp_int': float(msg_payload.split('/')[2]),
                '_temp_ext': float(msg_payload.split('/')[3]),
                '_out_0': bool(msg_payload.split('/')[4]),
                '_out_1': bool(msg_payload.split('/')[5]),
                'update_server' : str(datetime.datetime.now())
                }
            print(doc)
        if msg_payload.split('/')[0] == '20':
            print("El tipo de mensaje es 20 y aun no sé que hacer")
        '''
        #time.sleep(3) #Suponiendo que el todo el proceso de almacenado dure 3 segundos
        #print(str(devices.find_one({'_id': pay.decode().split('/')[0]})).split(',')[1].split(':')[1].split("'")[1]) #Obtengo e imprimo el nombre del usuario del Tempec que ha enviado msg
        logging.info(f"IF- Terminamos la tarea con el msg {msg_payload} y el topic {msg_topic}" ) #Aqui imprimo cuando se termina la tarea y con que Thread se termino la tarea
    else:
        logging.info(f"ELSE- Terminamos la tarea con el msg {msg_payload} y el topic {msg_topic}" ) #Aqui imprimo cuando se termina la tarea y con que Thread se termino la tarea
        #print("El dispositivo no con el _id = " + msg_payload.split('/')[1] + " no existe.")
    

def on_connect(client, userdata, flags,rc):
    client.subscribe("Tempec/Server")
    #client.publish("Celular/jojo/3", "Inicio de Trabajo ---> Fecha:" + str(datetime.now()))
    print("Tonight's the night")

def on_message(client, userdata, msg):
    #print(str(client))
    #print(str(userdata))
    print(str(datetime.now()))
    executor.submit(somebody_save_me, msg.payload.decode(), msg.topic)

executor = ThreadPoolExecutor(max_workers=2)
monzav = mqtt.Client()
monzav.on_connect = on_connect
monzav.on_message = on_message
monzav.connect("test.mosquitto.org", 1883, 60)
#monzav.loop_start() #once
monzav.loop_forever()

'''
    #10/AAA002/16.7/29.0/0/0
    #20/AAA001/16.0/0.5/0.5
    #id:name:setpoint:temp_ext:temp_int:out_0:out_1:his_h:his_l:temp_min:date_min:temp_max:date_max:update_server  
    #col.insert_one(doc)  
    #print("Mensaje Insertado "  + msg.payload.decode() + " / " + str(datetime.datetime.now()))
    #print(str(datetime.date.today()))
    #print(str(datetime.datetime.now().hour))
'''