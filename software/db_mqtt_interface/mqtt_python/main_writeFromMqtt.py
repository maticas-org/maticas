# importa dirty8w8 que tiene las credenciales
# ni por el putas vayan a subir 'dirty8w8.py'
from dirty8w8 import *
from dotenv import load_dotenv
from writeFromMqtt import mqtt_broker_connection_write

load_dotenv()
send_conn = mqtt_broker_connection_write( mqtt_broker = os.environ['MQTT_BROKER'],
                                          mqtt_port = os.environ['MQTT_PORT'],
                                          mqtt_username = os.environ['MQTT_USERNAME'],
                                          mqtt_password = os.environ['MQTT_PASSWORD'],
                                          mqtt_client_id = os.environ['MQTT_CLIENT_ID']
                                          )

send_conn.send_message(alias_topic = 'light', message = '1')
send_conn.send_message(alias_topic = 'light', message = '0')
send_conn.send_message(alias_topic = 'pump', message = '1')
send_conn.send_message(alias_topic = 'pump', message = '0')
