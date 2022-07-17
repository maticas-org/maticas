########################################
from time import sleep
import paho.mqtt.client as paho
from paho import mqtt
from sys import path
from os.path import abspath, dirname
########################################

# the directory where the database is defined to the path
current_file_directory = dirname(abspath(__file__))
client_mqtt_def_dir = "/mqtt_python"
db_def_dir          = "/db"

path.append(current_file_directory + client_mqtt_def_dir)
path.append(current_file_directory + db_def_dir)

from db_connection import DbConnection
from mqtt_client import MqttClient


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

        self.mqtt_conn = MqttClient(mqtt_broker     = mqtt_broker,
                                    mqtt_port       = mqtt_port,
                                    mqtt_username   = mqtt_username,
                                    mqtt_password   = mqtt_password,
                                    mqtt_client_id  = mqtt_client_id) 
        
        self.db_conn = DbConnection(db_host        = db_host,
                                    db_name        = db_name,
                                    db_user        = db_user,
                                    db_password    = db_password,
                                    db_sslmode     = db_sslmode)

        self.mqtt_conn.set_on_message(self.on_message)
        

    def on_message(self, client, userdata, message) -> None:


        # decodes the message
        msg = str(message.payload.decode("utf-8"))       
        msg = msg.strip(' ')

        # gets the topic
        topic = message.topic                           

        #gets the alias, which is expected to be the last part of the topic
        alias = topic.split("/")[-1]

        #recieved message, its topic and its qos 
        print(f"Message received: {msg} from topic: {topic} with QoS: {message.qos}")

        self.db_conn.write_data(value = float(msg), alias = alias, verbose = True)

    def start(self) -> None:

        while True:
            sleep(0.25)



