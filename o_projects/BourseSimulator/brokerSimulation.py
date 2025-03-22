import paho.mqtt.client as mqtt
import os
import time
from threading import Thread

MQTT_BROKER = "mqtt.eclipseprojects.io"
num_banks = int(os.getenv("NUM_BANKS",0))
counter = [[0,0]* num_banks]

def on_message(client, userdata, message):
    topic = message.topic.split("/")
    if topic[0] == "help":
        payload = int(message.payload.decode("utf-8"))
        counter[int(topic[1])][0] += 1
        counter[int(topic[1])][1] += payload
        
        if counter[int(topic[1])][0] == (num_banks-1):
            client.publish(f"portfoliohelper/{int(topic[1])}", counter[int(topic[1])][1])
            counter[int(topic[1])][0] = 0
            counter[int(topic[1])][1] = 0
              
client = mqtt.Client(f"broker")
client.connect(MQTT_BROKER)

client.loop_start()
for index in range(num_banks):
    client.subscribe(f"help/{index}")
client.on_message = on_message
time.sleep(999999)
    
#client.publish(f"portfolio/{my_bank}",activeBank.portfolio)