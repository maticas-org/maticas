# dirty7w7 contiene las credenciales
# ni por el putas suban al git 'dirty7w7.py'
# from dirty7w7 import *
from  db_connection import db_connection
from dotenv import load_dotenv
import os
load_dotenv()
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_SSLMODE = os.getenv("DB_SSLMODE")



conn = db_connection(db_host =  os.getenv("DB_HOST"),
                     db_name =  os.getenv("DB_NAME"),
                     db_user = os.getenv("DB_USER"),
                     db_password = os.getenv("DB_PASSWORD"),
                     db_sslmode = os.getenv("DB_SSLMODE")
                    )

conn.create_tables()
conn.default_table_initialization()
#conn.drop_all_data_tables()


#######################################################
print(
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'hum',
               verbose = True)
)

#######################################################
print(
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'temp',
               verbose = True)
)

#######################################################
print(
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'lux',
               verbose = True)
)

#######################################################
print(
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'pressure',
               verbose = True)
)


print('\n\n\n')
"""
##########################################################
#                   Escribiendo settings
##########################################################



conn.write_ambiental_settings(value_min = 60,
                                value_max = 70,
                                config_   = 'hum_optimal',
                                verbose = True)

conn.write_ambiental_settings(value_min = 50,
                                value_max = 80,
                                config_   = 'hum_ok',
                                verbose = True)


conn.write_actuators_settings(config_ = 'pump',
                              params = ('6:00:00', 
                                        '20:00:00', 
                                        40, 
                                        10),
                              verbose = True
                              )
print('-'*50)
print('\n\n')

conn.write_actuators_settings(config_ = 'lights',
                              params = ('17:00:00', 
                                        '20:00:00'),
                              verbose = True
                              )

print('-'*50)
print('\n\n')



##########################################################
#                  Leyendo los settings 
##########################################################

print( conn.read_ambiental_settings(config_ = 'hum_optimal', verbose = True) )

print( conn.read_ambiental_settings(config_ = 'hum_ok', verbose = True) )

print('-'*50)
print('\n\n')


print( conn.read_actuators_settings(config_ = 'pump') )

print( conn.read_actuators_settings(config_ = 'lights') )
"""
conn.end_connection()

