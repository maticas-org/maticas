# se trae las sucias credenciales
from db import dirty7w7 
from mqtt_python import dirty8w8 

from db_mqtt import mqtt_broker_and_db_connection

mqtt_conn = mqtt_broker_and_db_connection(  mqtt_broker     = dirty8w8.mqtt_broker, 
                                            mqtt_port       = dirty8w8.mqtt_port,
                                            mqtt_username   = dirty8w8.mqtt_username,
                                            mqtt_password   = dirty8w8.mqtt_password,
                                            mqtt_client_id  = dirty8w8.mqtt_client_id, 
                                            db_host         = dirty7w7.db_host,
                                            db_name         = dirty7w7.db_name,
                                            db_user         = dirty7w7.db_user,
                                            db_password     = dirty7w7.db_password,
                                            db_sslmode      = dirty7w7.db_sslmode,
                                         )


