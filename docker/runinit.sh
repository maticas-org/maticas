#!/bin/bash
mosquitto -c /etc/mosquitto/mosquitto.conf -d
/etc/init.d/postgresql start 
cd /app/software/db_mqtt_interface/
python main_db_mqtt.py &
cd /app/software/daemon
python origami.py &
cd /app/software/app_web/
python main_web_huerta.py
