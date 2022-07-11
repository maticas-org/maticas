#!/bin/bash

nohup python3 ./db_mqtt_interface/main_db_mqtt.py &> ./nohup.out &

cd  ./daemon
nohup python3 origami.py &> ./nohup.out &

