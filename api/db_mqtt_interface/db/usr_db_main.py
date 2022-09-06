from  db_connection_users import *
from dotenv import load_dotenv
import os
load_dotenv()

usr_conn = DbConnectionUsers( db_host =  os.getenv("USR_DB_HOST"),
                              db_name =  os.getenv("USR_DB_NAME"),
                              db_user =  os.getenv("USR_DB_USER"),
                              db_password = os.getenv("USR_DB_PASSWORD"),
                              db_sslmode  = os.getenv("USR_DB_SSLMODE") )

result = usr_conn.add_user(username = "test_usr1000",
                           email    = "usr1000@gmail.com",
                           password = "I'mUserNumber1000")

print(result)

usr_conn.auth_user_by_username(username = "test_usr1000",
                               password = "I'mUserNumber1000")
