#!/bin/bash

nohup python3 /home/dave/db_mqtt_interface/main_db_mqtt.py &> /home/dave/nohup.out &

cd  /home/dave/daemon
nohup python3 origami.py &> ./nohup.out &
