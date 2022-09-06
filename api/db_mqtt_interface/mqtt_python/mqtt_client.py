import csv
from pprint import pprint as pp
import datetime
import time 

import paho.mqtt.client as paho
from paho import mqtt

#------------------------------------#
import os
from dotenv import load_dotenv


class MqttClient():

    """
        This class gets messages from the MQTT broker 
        and retrieves them.
    """

    def __init__(self,
                 mqtt_broker: str,
                 mqtt_port: int, 
                 mqtt_username: str,
                 mqtt_password: str,
                 mqtt_client_id: str):

        print("creating client ...")

        # definición del broker a usar 
        # ip del broker en red local
        self.mqttBroker = mqtt_broker

        self.client = paho.Client( client_id = mqtt_client_id,
                                   userdata  = None,
                                   protocol  = paho.MQTTv5 )

        self.client.on_message = self._on_message
        self.client.on_connect = self.on_connect

        print("\t on_message set")
        print("\t on_connect set")

        # habilita conexión segura con tls
        #self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        print("loging into broker ...")
        self.client.username_pw_set(username = mqtt_username,
                                    password = mqtt_password)

        #connects asynchronously to the broker
        self.client.connect_async(self.mqttBroker, mqtt_port, keepalive=60)

        # by then calling client.loop_start() the client will run a loop 
        # in a background thread. This loop will take care of calling
        # client.on_connect() and client.on_message()
        self.client.loop_start()

        print("connected to broker.")
        print("-"*60)

    #-------------------------------------------------------------------------#
    #                                                                         #
    #-------------------------------------------------------------------------#

    def get_subscribe_topics(self):

        """
            This method gets and adds the subscribe topics 
            from the .env file.
        """

        load_dotenv()

        # gets the topics from the .env file
        self.subscribe_topics   = os.environ['MQTT_SUB_TOPICS']
        # separates the topics and puts them in a list
        self.subscribe_topics   = self.subscribe_topics.split(';')
        
        place_holder = []

        # removes the empty strings and undesired spaces from the list
        for topic in self.subscribe_topics:
            place_holder.append( topic.strip(' ').strip('\n').strip('\t') )

        self.subscribe_topics = place_holder

        print("Found the following subscribe topics:")
        print(self.subscribe_topics)


    def set_on_message(self, func):
        self.client.on_message = func


    def set_send_message(self, func):
        self.client.on_message = func

    #-------------------------------------------------------------------------#
    #                                                                         #
    #-------------------------------------------------------------------------#

    def on_connect(self, client, userdata, flags, rc, properties=None):

        print("Connected with result code "+str(rc))

        # subscribes to the topics
        self.get_subscribe_topics()

        for topic in self.subscribe_topics:
            self.client.subscribe(topic, qos = 2)
            print(f"Subscribed to topic: {topic}.\n")
        
        print("-"*60)


    def send_message(self, topic: str, message: str, qos = 2) -> None:

        self.client.publish(topic, message, qos)
        time.sleep(0.1) 


    def _on_message(self, client, userdata, message) -> None:

        # decodes the message
        msg = str(message.payload.decode("utf-8"))       
        msg = msg.strip(' ')

        # gets the topic
        topic = message.topic                           

        #recieved message, its topic and its qos 
        print(f"Message received: {msg} from topic: {topic} with QoS: {message.qos}")
        



        






