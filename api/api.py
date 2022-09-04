from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema, Float
from db.db_connection import DbConnection
from dotenv import load_dotenv
import os
load_dotenv()

conn = DbConnection( db_host =  os.getenv("DB_HOST"),
                     db_name =  os.getenv("DB_NAME"),
                     db_user = os.getenv("DB_USER"),
                     db_password = os.getenv("DB_PASSWORD"),
                     db_sslmode = os.getenv("DB_SSLMODE") )


class Query(ObjectType):

    hello    = String(name = String(default_value = "stranger"))
    goodbye  = String()
    ambient_variable  = String(var = String(default_value = "temperature"), 
                               timestart  = String(), 
                               timefinish = String())

    create_ambiental_variable_table = String(table_name = String(),
                                             mqtt_topic = String(),
                                             mqtt_send_message_frecuency =  String(), 
                                             precision = String())
    
    def resolve_hello(root, info,
                      name: str) -> str:
        return f'Hello {name}!'

    def resolve_goodbye(root, info) -> str:
        return 'See ya!'

    def resolve_ambient_variable(root, info, 
                                 var: str,
                                 timestart: str,
                                 timefinish: str) -> str:
        """
            Get ambient data from the database.

                INPUT:  var         - variable to get data from
                        timestart   - start time of the data
                        timefinish  - finish time of the data

                OUTPUT: ambient data from the database.
        """

        result = conn.read_data(table_name = var, 
                                timestamp_start = timestart,
                                timestamp_end   = timefinish)

        return result
    
    def resolve_create_ambiental_variable_table(root, 
                                                info,
                                                table_name: str,
                                                mqtt_topic: str,
                                                mqtt_send_message_frecuency: str, 
                                                precision = 3) -> dict:
                              
        """
            Create ambiental variable table on request from API.
            an mqtt_topic, and mqtt_send_message_frecuency must be specified for 
            configuration of mqtt server.

            INPUT:
                    - table_name:   Name of the table which is going to be created.
                    - mqtt_topic:   MQTT topic on which the information is going to arrive from the sensors.
                    - mqtt_send_message_frecuency:  Frecuency on which we expect the messages to arrive, 
                                                    For example: 1 every minute, or 1 every half a minute.
                    - precision:    Floating point precision of the data.

            OUTPUT:
                    dictionary with this shape: {"exit_status": "answer"}
        """

        result = conn.create_ambiental_variable_table(table_name = table_name,
                                                      precision = precision)


        return result








"""
Example query:

    {
        ambientVariable(var: "temperature_var", 
                        timestart: "1999/12/12 00:00:00",
                        timefinish: "2021/12/12 00:00:00"),
        createAmbientalVariableTable(tableName: "rain_var",
                                     mqttTopic: "/esp31/data/rain",
                                     mqttSendMessageFrecuency: "0.5",
                                     precision: "3"),
        hello,
        goodbye
    }
"""

