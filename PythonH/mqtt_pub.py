import time
import paho.mqtt.client as paho
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print(client + " Conectado... <3")
    client.publish("Monzav/Server", "Hola Corazon")

client = paho.Client(client_id="Alienware2", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("Monzav", "mqtt057447")
client.connect("9db78e371b064745883b9e4ede7be333.s2.eu.hivemq.cloud", 8883)

client.on_connect = on_connect
