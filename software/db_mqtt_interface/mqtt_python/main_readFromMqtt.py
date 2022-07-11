# importa dirty8w8 que tiene las credenciales
# ni por el putas vayan a subir 'dirty8w8.py'
from dirty8w8 import *
from dotenv import load_dotenv
from readFromMqtt import mqtt_broker_connection

load_dotenv()
mqtt_conn = mqtt_broker_connection( mqtt_broker = os.environ['MQTT_BROKER'],
                                    mqtt_port = os.environ['MQTT_PORT'],
                                    mqtt_username = os.environ['MQTT_USERNAME'],
                                    mqtt_password = os.environ['MQTT_PASSWORD'],
                                    mqtt_client_id = os.environ['MQTT_CLIENT_ID']
                                    )






