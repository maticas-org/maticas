# se trae las sucias credenciales
from dotenv import load_dotenv
from db_mqtt import mqtt_broker_and_db_connection
import os

load_dotenv()
mqtt_conn = mqtt_broker_and_db_connection(  mqtt_broker     = os.getenv("MQTT_BROKER"),
                                            mqtt_port       = int(os.getenv("MQTT_PORT")),
                                            mqtt_username   = os.getenv("MQTT_USERNAME"),
                                            mqtt_password   = os.getenv("MQTT_PASSWORD"),
                                            mqtt_client_id  = os.getenv("MQTT_CLIENT_ID"),
                                            db_host         = os.getenv("DB_HOST"),
                                            db_name         = os.getenv("DB_NAME"),
                                            db_user         = os.getenv("DB_USER"),
                                            db_password     = os.getenv("DB_PASSWORD"),
                                            db_sslmode      = os.getenv("DB_SSLMODE"),
                                         )
mqtt_conn.start()


