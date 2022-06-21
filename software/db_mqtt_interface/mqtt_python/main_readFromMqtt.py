# remember that dirty7w7 contains the database credentials 
# don't ever think of uploading the credentials to the github repository, 
# just in case I'll add the credentials to the .gitignore

import json
from readFromMqtt import mqtt_broker_connection

with open('./dirty8w8.json') as f:
    mqtt_credentials = json.load(f)

mqtt_conn = mqtt_broker_connection( mqtt_broker     = mqtt_credentials["mqtt_broker"],
                                    mqtt_port       = mqtt_credentials["mqtt_port"],
                                    mqtt_username   = mqtt_credentials["mqtt_username"],
                                    mqtt_password   = mqtt_credentials["mqtt_password"],
                                    mqtt_client_id  = mqtt_credentials["mqtt_client_id"] 
                                    )






