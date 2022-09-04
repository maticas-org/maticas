#!/bin/bash

initiate_dotenv(){
    echo "$1" > .env
}

append_to_dotenv(){
    echo "$1" >> .env
}

# 7w7
initiate_dotenv "DB_HOST='localhost'"
append_to_dotenv "DB_NAME='maticas'"
append_to_dotenv "DB_USER='dave'"
append_to_dotenv "DB_PASSWORD='0000'"
append_to_dotenv "DB_SSLMODE='disable'"

# 8W8
append_to_dotenv "MQTT_BROKER='localhost'"
append_to_dotenv "MQTT_PORT=1883"
append_to_dotenv "MQTT_USERNAME='dio'"
append_to_dotenv "MQTT_PASSWORD='123'"
append_to_dotenv "MQTT_CLIENT_ID='listener'"

#path to files
append_to_dotenv "DB_DEPENDENCIES1_PATH= '$(pwd)/software/db/define_db'"
append_to_dotenv "DB_DEPENDENCIES2_PATH= '$(pwd)/software/db/database_backup'"
append_to_dotenv "MQTT_SUB_TOPICS='esp32data/measure/ph; esp32data/measure/ec; esp32data/measure/wtemp; \
                                   esp82data/measure/lux; esp82data/measure/temp; esp82data/measure/hum; \
                                   esp82data/measure/pressure'"

