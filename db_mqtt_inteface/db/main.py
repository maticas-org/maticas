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

#######################################################
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'hum',
               verbose = True)

#######################################################
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'temp',
               verbose = True)

#######################################################
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'lux',
               verbose = True)

#######################################################
conn.read_data(timestamp_start = '2020-01-01 00:00:00',
               timestamp_end   = '2029-01-01 00:00:00',
               type_ = 'pressure',
               verbose = True)



conn.end_connection()


