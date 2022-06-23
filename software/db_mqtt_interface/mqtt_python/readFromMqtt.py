import csv
from pprint import pprint as pp
import datetime
import time 
import logging
import json

import paho.mqtt.client as paho
from paho import mqtt


class mqtt_broker_connection():

    """
        Clase que recibe los mensajes de del broker 
        MQTT y los muestra, el código de esta clase 
        es la base para el usado en 'maticas/db_mqtt_inteface/main_db_mqtt.py'
        que básicamente recibe mensajes del broker mqtt y los guarda en la base
        de datos de postgres.
    """

    def __init__(self,
                 mqtt_broker: str,
                 mqtt_port: int, 
                 mqtt_username: str,
                 mqtt_password: str,
                 mqtt_client_id: str):

        # diccionario para guardar los mensajes que llegan de una forma más ordenada
        # los valores de las llaves en el diccionario serán los códigos que identifican a cada sensor
        self.messages = {}

        # definición del broker a usar 
        # ip del broker en red local
        self.mqttBroker = mqtt_broker

        logging.info("MQTT: Setting up paho client with credentials ...")
        self.client = paho.Client( client_id= mqtt_client_id,
                                   userdata = None,
                                   protocol = paho.MQTTv5 )
        logging.info("MQTT: Defining on_message and on_connect actions ...")
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        # habilita conexión segura con tls
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        logging.info("MQTT: Logging as user to the broker ...")
        self.client.username_pw_set(username = mqtt_username,
                                    password = mqtt_password)

        #gets connected to the broker
        logging.info("MQTT: Stablishing connection to the broker ...")
        self.client.connect(self.mqttBroker, mqtt_port) 

        logging.info("MQTT: Reading publish settings ...")
        
        self.mqtt_subscribe_topics = './topics_settings/sub_topics.json'

        with open(self.mqtt_subscribe_topics) as f:
            self.subscribe_topics = json.load(f)

        logging.info("MQTT: Done setup.")
        logging.info("MQTT: Starting listening loop...")
        self.client.loop_forever()


    def on_connect(self, client, userdata, flags, rc, properties=None):

        logging.info("MQTT: Connected with result code {}.".format(rc))
        print("MQTT: Connected with result code {}.".format(rc))

        #subscripción a todos los temas de la forma 'Esp8266!D4ta/*'
        #que se encuentran dentro del diccionario de temas especificados

        logging.info("MQTT: Suscribing to all topics from {}".format(self.mqtt_subscribe_topics) )
        topics = list(self.subscribe_topics.values())

        for topic in topics:
            self.client.subscribe(topic, qos = 2)              

    def on_message(self, client, userdata, message):

        # limpia el diccionario de mensajes
        self.messages.clear()


        msg = str(message.payload.decode("utf-8"))      #decodificación del mensaje enviado 
        msg = msg.strip(' ')
        topic = message.topic                           #obtención del tema de llegada del mensaje

        topic = topic.split('/')                        #obtención de la información importante que se encuentra
        topic = topic[1:]                               #expresada en el tema del mensajede llegada
                                                        #esto es de la forma: ['10370001','pressure']

        logging.info( "MQTT:MSG: Arrived {}".format(topic) )

        print(topic)
        #agrego valores a la llave dada por el id del sensor (topic[0] contiene el id del sensor)
        #lo que contiene messages[topic[0]] es de la forma ['temperatura', 'humedad', 'presión atmosférica', 'lux']

        if topic[0] in self.messages.keys():
            self.messages[topic[0]][topic[1]] = msg 

        else:
            self.messages[topic[0]] = {}
            self.messages[topic[0]][topic[1]] = msg

        print('---'*20)







