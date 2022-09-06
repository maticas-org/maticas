from  db_connection import DbConnection
from dotenv import load_dotenv
import os
load_dotenv()

conn = DbConnection( db_host =  os.getenv("DB_HOST"),
                     db_name =  os.getenv("DB_NAME"),
                     db_user = os.getenv("DB_USER"),
                     db_password = os.getenv("DB_PASSWORD"),
                     db_sslmode = os.getenv("DB_SSLMODE") )


