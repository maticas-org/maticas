# importa dirty8w8 que tiene las credenciales
# ni por el putas vayan a subir 'dirty8w8.py'
from dirty8w8 import *
from writeFromMqtt import mqtt_broker_connection_write


send_conn = mqtt_broker_connection_write( mqtt_broker = mqtt_broker,
                                          mqtt_port = mqtt_port,
                                          mqtt_username = mqtt_username,
                                          mqtt_password = mqtt_password,
                                          mqtt_client_id = mqtt_client_id 
                                          )

send_conn.send_message(alias_topic = 'light', message = '1')
send_conn.send_message(alias_topic = 'light', message = '0')
send_conn.send_message(alias_topic = 'pump', message = '1')
send_conn.send_message(alias_topic = 'pump', message = '0')
