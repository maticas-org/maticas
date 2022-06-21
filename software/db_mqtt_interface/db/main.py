# remember that dirty7w7 contains the database credentials 
# don't ever think of uploading the credentials to the github repository, 
# just in case I'll add the credentials to the .gitignore

import json
from  db_connection import db_connection

with open('./dirty7w7.json') as f:
    db_credentials = json.load(f)

conn = db_connection(db_host        =  db_credentials["db_host"],
                     db_name        =  db_credentials["db_name"],
                     db_user        =  db_credentials["db_user"],
                     db_password    =  db_credentials["db_password"],
                     db_sslmode     =  db_credentials["db_sslmode"],
                    )

# creates the database tables in case they don't exist
conn.create_tables()

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


