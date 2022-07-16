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

conn.create_tables()
conn.insert_default_data()




