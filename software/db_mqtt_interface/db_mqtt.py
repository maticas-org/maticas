########################################
import csv
from pprint import pprint as pp
import datetime
import time 

import paho.mqtt.client as paho
from paho import mqtt
########################################

from db import db_connection as db_conn

class mqtt_broker_and_db_connection():

    def __init__(self,
                 mqtt_broker: str,
                 mqtt_port: int, 
                 mqtt_username: str,
                 mqtt_password: str,
                 mqtt_client_id: str,
                 db_host: str, 
                 db_name: str,
                 db_user: str, 
                 db_password: str,
                 db_sslmode: str):

        # diccionario para guardar los mensajes que llegan de una forma más ordenada
        # los valores de las llaves en el diccionario serán los códigos que identifican a cada sensor
        self.messages = {}

        # Conexión con la base de datos de azure
        self.db_conn = db_conn.db_connection(db_host =  db_host,
                                             db_name =  db_name,
                                             db_user = db_user,
                                             db_password =  db_password,
                                             db_sslmode = db_sslmode,
                                            )

        # definición del broker a usar 
        # ip del broker en red local
        self.mqttBroker = mqtt_broker

        self.client = paho.Client( client_id= mqtt_client_id,
                                   userdata = None,
                                   protocol = paho.MQTTv5 )
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        # habilita conexión segura con tls
        # self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        self.client.username_pw_set(username = mqtt_username,
                                    password = mqtt_password)
        #conexión al broker
        self.client.connect(self.mqttBroker, mqtt_port) 
        self.client.loop_forever()



    def on_connect(self, client, userdata, flags, rc, properties=None):

        print("Connected with result code "+str(rc))

        #subscripción a todos los temas de la forma 'Esp8266!D4ta/*'
        self.client.subscribe("Esp8266!D4ta/#")              

    def on_message(self, client, userdata, message):


        msg = str(message.payload.decode("utf-8"))      #decodificación del mensaje enviado 
        msg = msg.strip(' ')
        topic = message.topic                           #obtención del tema de llegada del mensaje

        topic = topic.split('/')                        #obtención de la información importante que se encuentra
        topic = topic[1:]                               #expresada en el tema del mensajede llegada
                                                        #esto es de la forma: ['10370001','pressure']

        print(topic)
        #agrego valores a la llave dada por el id del sensor (topic[0] contiene el id del sensor)
        #lo que contiene messages[topic[0]] es de la forma ['temperatura', 'humedad', 'presión atmosférica', 'lux']

        if topic[0] in self.messages.keys():
            self.messages[topic[0]][topic[1]] = msg 

        else:
            self.messages[topic[0]] = {}
            self.messages[topic[0]][topic[1]] = msg

        self.db_conn.write_data( value = float(msg),
                                 type_ = topic[1] ) 


        # limpia el diccionario de mensajes
        self.messages.clear()



