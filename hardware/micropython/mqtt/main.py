
from mqtt import MqttConnection
from json import load
from time import sleep

with open('./mqtt_config.json') as f:
    mqtt_config = load(f)

mqtt_client = MqttConnection(**mqtt_config)

# connects esp32 to the MQTT broker
mqtt_client.mqtt_connect()

while True:

    mqtt_client.publish('test', 'test')
    sleep(1)
