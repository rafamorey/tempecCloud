import time
import paho.mqtt.client as paho
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print("Conectado... <3")

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# def on_subscribe(client, userdata, mid, granted_qos, properties=None):
#     print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + "end <3")

client = paho.Client(client_id="Alienware", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("Monzav", "mqtt057447")
client.connect("9db78e371b064745883b9e4ede7be333.s2.eu.hivemq.cloud", 8883)

# client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.on_connect = on_connect

client.subscribe("Tempec/Server") #, qos=1)

#client.publish("encyclopedia/temperature", payload="hot", qos=1)
client.loop_forever()