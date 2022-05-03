# importa dirty8w8 que tiene las credenciales
# ni por el putas vayan a subir 'dirty8w8.py'
from dirty8w8 import *
from readFromMqtt import mqtt_broker_connection

mqtt_conn = mqtt_broker_connection( mqtt_broker = mqtt_broker,
                                    mqtt_port = mqtt_port,
                                    mqtt_username = mqtt_username,
                                    mqtt_password = mqtt_password,
                                    mqtt_client_id = mqtt_client_id 
                                    )






