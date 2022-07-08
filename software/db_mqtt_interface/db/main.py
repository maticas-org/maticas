# dirty7w7 contiene las credenciales
# ni por el putas suban al git 'dirty7w7.py'
from dirty7w7 import *
from  db_connection import db_connection


conn = db_connection(db_host =  db_host,
                     db_name =  db_name,
                     db_user = db_user,
                     db_password =  db_password,
                     db_sslmode = db_sslmode,
                    )

conn.create_tables()
#conn.default_table_initialization()
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

conn.end_connection()

