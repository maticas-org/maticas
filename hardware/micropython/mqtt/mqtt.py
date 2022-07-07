# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()



class MqttConnection():
    def __init__(self,
                 wifi_ssid:         str,
                 wifi_password:     str,
                 client_id:         str,
                 mqtt_server:       str,
                 client_password =  None,
                 port =             1883,
                 user =             None, 
                 keepalive =        30,
                 clean_session =    True, 
                 ssl =             False,
                 ssl_params =       {},
                 pub_topics =       {}, 
                 sub_topics =       {}      ): 

        # stores parameters inside class
        self.wifi_ssid          = wifi_ssid 
        self.wifi_password      = wifi_password
        self.client_id          = client_id
        self.mqtt_server        = mqtt_server 
        self.port               = port 
        self.user               = user 
        self.client_password    = client_password
        self.keepalive          = keepalive
        self.ssl                = ssl
        self.ssl_params         = ssl_params
        self.pub_topics         = pub_topics
        self.sub_topics         = sub_topics
        self.clean_session      = clean_session

        # starts internet connection in order to connect to the mqtt server
        #self.start_internet_connection()

        # creates the mqtt client
        self.client = MQTTClient(client_id, mqtt_server, port, user, client_password, keepalive, ssl, ssl_params)

        # configures the mqtt client

        # last will message, if the client disconnects this message will be published
        # just before that
        self.client.set_last_will(topic  = 'notification', 
                                  msg    = 'offline',
                                  qos    = 1,
                                  retain = True)

        self.client.set_callback(self._callback)

        self.last_arrive_topic      = None
        self.last_recieved_message  = None

        # starts mqtt connection 
        # self.mqtt_connect()
    

    def start_internet_connection(self):

        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        self.station.connect(self.wifi_ssid, self.wifi_password)

        while self.station.isconnected() == False:
          pass

        print('Successfull connection to network!')
        print(self.station.ifconfig())

    def mqtt_connect(self):
        self.client.connect(clean_session = self.clean_session)
        print('Successfull connection to MQTT broker!')


    def _callback(self, topic, msg):
        self.last_arrive_topic      = topic
        self.last_recieved_message  = msg

        print('Received message {1} on topic: {0}'.format(topic, msg))
    
    
    def publish(self, topic, msg, retain=False, qos=1):
        self.client.publish(topic, msg, retain, qos)

    def subscribe(self):

        # subscribes to all topics in the sub_topics dictionary
        # getting also the specified qos
        for topic in self.sub_topics.values():
            self.client.subscribe(topic = topic, 
                                  qos   = self.sub_topics[topic][qos])

    
    def set_last_will(self, topic, msg, retain=False, qos=0):
        self.client.set_last_will(topic, msg, retain, qos)
    
    def set_callback(self, callback):
        self.client.set_callback(callback)
        print("Successfull connection to broker!")
    
