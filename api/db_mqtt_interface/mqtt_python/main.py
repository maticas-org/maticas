import os
from dotenv import load_dotenv
from mqtt_client import MqttClient
from time import sleep

load_dotenv()

mqtt_conn = MqttClient( mqtt_broker     = "192.168.1.105",
                        mqtt_port       = 1883,
                        mqtt_username   = os.environ['MQTT_USERNAME'],
                        mqtt_password   = os.environ['MQTT_PASSWORD'],
                        mqtt_client_id  = os.environ['MQTT_CLIENT_ID'] ) 

while True:

    mqtt_conn.send_message(topic = "hello",
                            message = "Hello World!",
                            qos = 2)
    sleep(0.250)


"""
mqtt_conn = MqttClient( mqtt_broker     = os.environ['MQTT_BROKER'],
                        mqtt_port       = int(os.environ['MQTT_PORT']),
                        mqtt_username   = os.environ['MQTT_USERNAME'],
                        mqtt_password   = os.environ['MQTT_PASSWORD'],
                        mqtt_client_id  = os.environ['MQTT_CLIENT_ID'] ) 
"""

