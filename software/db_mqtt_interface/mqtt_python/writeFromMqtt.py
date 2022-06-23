import pandas as pd
import time 
from datetime import datetime as dt
import logging

import paho.mqtt.client as paho
from paho import mqtt
import json

class mqtt_broker_connection_write():

    """
        Clase para conectarse al broker mqtt y enviar mensajes a los actuadores, 
        a saber: 
        1. Luces
        2. Bomba de agua
        3. Bombas de agua que controlan Ph y Nivel de nutriente
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
        self.mqtt_port  = mqtt_port

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

        #conexión al broker
        logging.info("MQTT: Stablishing connection to the broker ...")
        self.client.connect(self.mqttBroker, mqtt_port) 

        """
        # Template of topics_dict data: 

        #-----------------------------------------------------------------------------
        #             'alias'         |  'tema para ese alias' 
        #-----------------------------------------------------------------------------

        self.topics_dict = {    'light':    'Esp8266!D4ta/10370005/lights',
                                'pump':     'Esp8266!D4ta/10370005/pump',
                                'ec_a':     'Esp8266!D4ta/10370007/pump/ec/a',
                                'ec_b':     'Esp8266!D4ta/10370007/pump/ec/b',
                                'ph_acid':  'Esp8266!D4ta/10370007/pump/ph/acid',
                                'ph_basic': 'Esp8266!D4ta/10370007/pump/ph/basic'
                           }
        """

        logging.info("MQTT: Reading publish settings ...")

        with open('./topics_settings/pub_topics.json') as f:
            self.topics_dict = json.load(f)

        logging.info("MQTT: Done setup.")


    def send_message(self, alias_topic: str, message: str, qos = 2):

        if alias_topic in self.topics_dict.keys():

            logging.info("MQTT: Connecting...")
            self.client.connect(self.mqttBroker, self.mqtt_port) 

            logging.info("MQTT:MSG: Sending message, qos = {}".format(qos))
            self.client.publish(self.topics_dict[alias_topic],
                                message, qos = 2)
            time.sleep(0.1) # wait


        else:

            print("Bad input ...")
            print("Keys are: ")
            print(self.topics_dict.keys())
            print("Got: ")
            print(alias_topic)

    def on_connect(self, client, userdata, flags, rc, properties=None):

        print("Connected with result code "+str(rc))

        #subscripción a todos los temas de la forma 'Esp8266!D4ta/*'
        self.client.subscribe("Esp8266!D4ta/#")              

    def on_message(self, client, userdata, message):

        # limpia el diccionario de mensajes
        self.messages.clear()

        msg = str(message.payload.decode("utf-8"))      #decodificación del mensaje enviado 
        msg = msg.strip(' ')
        topic = message.topic                           #obtención del tema de llegada del mensaje

        topic = topic.split('/')                        #obtención de la información importante que se encuentra
        topic = topic[1:]                               #expresada en el tema del mensajede llegada
                                                        #esto es de la forma: ['10370001','pressure']

        logging.info("MQTT:MSG: Arrived {}".format(topic))
        print(topic)
        print(msg)
        #agrego valores a la llave dada por el id del sensor (topic[0] contiene el id del sensor)
        #lo que contiene messages[topic[0]] es de la forma ['temperatura', 'humedad', 'presión atmosférica', 'lux']

        if topic[0] in self.messages.keys():
            self.messages[topic[0]][topic[1]] = msg 

        else:
            self.messages[topic[0]] = {}
            self.messages[topic[0]][topic[1]] = msg

        print('---'*20)





