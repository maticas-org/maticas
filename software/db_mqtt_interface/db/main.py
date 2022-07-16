from  db_connection import DbConnection
from dotenv import load_dotenv
import os
load_dotenv()
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_SSLMODE = os.getenv("DB_SSLMODE")



conn = DbConnection( db_host =  os.getenv("DB_HOST"),
                     db_name =  os.getenv("DB_NAME"),
                     db_user = os.getenv("DB_USER"),
                     db_password = os.getenv("DB_PASSWORD"),
                     db_sslmode = os.getenv("DB_SSLMODE") )

conn.write_actuators_settings(alias = "pump", 
                              params = {'start_time':   '07:00:00',
                                        'end_time':     '20:00:00',
                                        'frequency':    45,
                                        'duration': 5})

conn.write_actuators_settings(alias = "lights", 
                              params = {'start_time':   '07:00:00',
                                        'end_time':     '20:00:00'})

for alias in conn.tables_actuators.keys():

    data = conn.read_actuators_settings(alias = alias)
    print(data.head())




