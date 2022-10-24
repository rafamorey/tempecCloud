from pydoc import cli
import time
import paho.mqtt.client as paho
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    monzav.subscribe("Monzav/1", qos=1)
    print("MQTT INICIADO")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

monzav = paho.Client(client_id="SoyElServer", userdata=None, protocol=paho.MQTTv5)
monzav.on_connect = on_connect

monzav.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
monzav.username_pw_set("Monzav", "Monzavmqtt")
monzav.connect("9db78e371b064745883b9e4ede7be333.s2.eu.hivemq.cloud", 8883)
monzav.on_message = on_message
monzav.loop_forever()