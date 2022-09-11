import datetime
import pytz
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, DateTime, Float, insert, select, delete

from sys import path
from os.path import abspath, dirname

# the directory where the database is defined to the path
current_file_directory = dirname(abspath(__file__))
database_definition_directory = current_file_directory + "/define_db"
path.append( database_definition_directory )

# imports database tables definitions 
from users_table        import *
from tables_utilities   import *


class UsrDbConnection():

    #-----------------------------------------------#
    # Initialization and configuration of the class #
    #-----------------------------------------------#

    def __init__(self, 
                 db_host: str,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_sslmode: str ):

        print("Starting Users database connection...")

        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_sslmode = db_sslmode
        self.metadata  = MetaData()

        conn_string = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
        print(conn_string)

        self.engine = create_engine(conn_string)
        self.configure_connection()

        print("Done creating Users database connection.")
        print("-"*60)
            

    def configure_connection(self) -> None:

        """
        """

        self.users_table = load_users_table(self.engine, self.metadata)

        if self.users_table == None:
            print("As no user table was found, one will be created...")
            self.users_table = Users(self.engine)


        print("Done starting the users database.")
        print("-"*60)


    ############################################################# 
    #-----------------------------------------------------------#
    #                                                           #
    #-----------------------------------------------------------#


    def add_user(self, username: str, email: str, password: str) -> None:

        """
        """

        result = self.users_table.insert_data(username = username,
                                              email    = email,
                                              password = password)

        return result




    def auth_user_by_username(self, username: str, password: str) -> str:

        """
        """

        result = self.users_table.auth_user_by_username(username = username,
                                                        password = password)

        return result


    def auth_user_by_email(self, username: str, password: str) -> str:

        """
        """

        return 0



