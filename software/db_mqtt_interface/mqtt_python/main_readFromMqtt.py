# remember that dirty7w7 contains the database credentials 
# don't ever think of uploading the credentials to the github repository, 
# just in case I'll add the credentials to the .gitignore

import json
from readFromMqtt import mqtt_broker_connection
import time
from datetime import datetime as dt
import logging

# sets the logging file 
logging.basicConfig( filename = 'mqtt_read.log',
                     encoding = 'utf-8',
                     level = logging.DEBUG,
                     filemode = 'w',
                     format='%(levelname)s:%(message)s')

logging.info("Started logging data at: {}".format(dt.today()))

# mqtt broker credentials
mqtt_credential_file = './dirty8w8.json'

# reads credentials from the file
with open(mqtt_credential_file) as f:

    logging.info("reading credentials {}".format(mqtt_credential_file))
    mqtt_credentials = json.load(f)



mqtt_conn = mqtt_broker_connection( mqtt_broker     = mqtt_credentials["mqtt_broker"],
                                    mqtt_port       = mqtt_credentials["mqtt_port"],
                                    mqtt_username   = mqtt_credentials["mqtt_username"],
                                    mqtt_password   = mqtt_credentials["mqtt_password"],
                                    mqtt_client_id  = mqtt_credentials["mqtt_client_id"] 
                                    )






