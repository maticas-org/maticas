# brings the dirty credentials

from db import dirty7w7 
from mqtt_python import dirty8w8 
from db_mqtt import mqtt_broker_and_db_connection


# loads the credentials from the mqtt broker and
# the postgres database

with open('./db/dirty7w7.json') as f:
    db_credentials = json.load(f)

with open('./mqtt_python/dirty8w8.json') as f:
    mqtt_credentials = json.load(f)


mqtt_conn = mqtt_broker_and_db_connection(  mqtt_broker     = mqtt_credentials["mqtt_broker"],
                                            mqtt_port       = mqtt_credentials["mqtt_port"],
                                            mqtt_username   = mqtt_credentials["mqtt_username"],
                                            mqtt_password   = mqtt_credentials["mqtt_password"],
                                            mqtt_client_id  = mqtt_credentials["mqtt_client_id"],
                                            db_host        =  db_credentials["db_host"],
                                            db_name        =  db_credentials["db_name"],
                                            db_user        =  db_credentials["db_user"],
                                            db_password    =  db_credentials["db_password"],
                                            db_sslmode     =  db_credentials["db_sslmode"],
                                         )


