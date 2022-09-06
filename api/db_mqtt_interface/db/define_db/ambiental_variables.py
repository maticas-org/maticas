from sqlalchemy import MetaData, Table, Column, DateTime, Float, insert, select, delete
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects import postgresql
import json

from os.path import abspath, dirname

# the directory where some data that can be used as default data
# is stored
current_file_dir = dirname(dirname(abspath(__file__)))
database_defult_data_dir = "database_backup_data"

default_data_path = current_file_dir + "/" + database_defult_data_dir

# utilite for unziping 
from zipfile import ZipFile


# -------------------------------------------
#   base class to inherit repetitive methods
#   to other variables.
# -------------------------------------------

"""
+-----------------------+-----------------+
|   time                |   column_name   |
+-----------------------+-----------------+
|                       |                 |
| "YYYY/MM/DD %H:%M:%S" | decimal_number  |
+-----------------------+-----------------+
"""
# now I need to override the initialization of a table
# and allow for the insertion of an already created table in the object
# Variable, in order to unlock all the previously implemented features.

class Variable():

    def __init__(self,
                 engine,
                 table_name:  str,
                 column:      str,
                 precision =  3):

        self.engine         = engine
        self.table_name     = table_name
        self.table_column   = column
        self.precision      = precision
        self.metadata_obj   = MetaData()
        self.create_table()


    def read_data(self,
                  timestamp_start: str,
                  timestamp_end: str) -> pd.DataFrame:

        """
            Reads data from the table, between the specified timestamps.
        """

        statement = select(self.table).\
                    where(self.table.c.time >= timestamp_start).\
                    where(self.table.c.time <= timestamp_end)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def create_table(self) -> None:
        """
            Create the table in the database.
        """

        self.table = Table( self.table_name,
                            self.metadata_obj,
                            Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                            Column(self.table_column, Float(precision = self.precision), nullable   = False),
                            extend_existing = True)

        self.metadata_obj.create_all(self.engine)


    def watch_dog(self, value) -> float:
        if value < 0:
            return -1


    def insert_data(self, value: float) -> int:

        """
            Inserts data into the table.

            if any error with the data it returns -1, 
            if a successfully inserted data it returns 0.
        """

        if watch_dog(value) == -1:
            return -1

        statement = insert(self.table).values(value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0



#
# same as the class above but creates an instance with all the previous functionalities 
# when the table is loaded directy from the database.
#

class Variable_From_DB(Variable):


    def __init__(self, engine, table: Table):

        self.engine = engine
        self.table  = table
        self.metadata_obj   = MetaData()

    def create_table(self) -> None:
            
        """
            Create the table in the database.
        """
        print("This table has already been created.")
        return 0








