import paho.mqtt.client as mqtt
#import multiprocessing
import time
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def super_task(pay, top):
    time.sleep(3)
    logging.info(f"Terminamos la tarea con el msg {pay} y el topic {top}" )

def on_connect(client, userdata, flags, rc):
    client.subscribe("Monzav/Server")

def on_message(client, userdata, msg):
    executor.submit(super_task, msg.payload, msg.topic)

executor = ThreadPoolExecutor(max_workers=2)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#lient.connect("mqtt.eclipseprojects.io", 1883, 60)
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()
