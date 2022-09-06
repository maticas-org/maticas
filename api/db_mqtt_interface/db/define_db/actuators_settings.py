from sqlalchemy import MetaData, Table, Column, DateTime, Time, Float, Integer, String, insert, select, delete
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects import postgresql

"""
+-----------------------+-----------------+----------------+---------------+--------------+------------------+
|   time                |   actuator      |   start_time   |   end_time    |   time_on    |   time_off       |
|-----------------------+-----------------+----------------+---------------+--------------+------------------+
|                       |                 |                |               |              |                  |
| "YYYY/MM/DD %H:%M:%S" | "actuator_name" |   "%H:%M:%S"   |  "%H:%M:%S"   |    nminutos  |     nminutos     |
+-----------------------+-----------------+----------------+---------------+--------------+------------------+
"""

class Actuators():

    def __init__(self, engine):

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'actuators_configuration',
                             self.metadata_obj,
                             Column("time",         DateTime,   default = datetime.utcnow),
                             Column("actuator",     String(60), nullable = False, primary_key = True),
                             Column("start_time",   Time,       nullable = False),
                             Column("end_time",     Time,       nullable = False),
                             Column("time_on",      Integer,    nullable = False),
                             Column("time_off",     Integer,    nullable = False))


    def insert_data(self, actuator:     str,
                          start_time:   str,
                          end_time:     str, 
                          time_on:      int,
                          time_off:     int) -> int:

        """
            Inserts data into the variable_ok table.
            
            returns 0 if everithing went ok,
                    -1 if there was an error.
        """

        if self.insert_data_watchdog(actuator, start_time, end_time, time_on, time_off) == -1:
            return -1

        # statement for insertion of new data
        insert_statement = insert(self.table).values(actuator   = actuator,
                                                     start_time = start_time,
                                                     end_time   = end_time,
                                                     time_on    = time_on,
                                                     time_off   = time_off)
                                                    
        # statement for deletion of previous data
        delete_statement = delete(self.table).where(self.table.c.actuator == actuator)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(delete_statement)
            connection.execute(insert_statement)

        return 0


    def read_data(self) -> pd.DataFrame:

        """
        Reads data from the humidity_ok table.
        """

        statement = select(self.table)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def insert_data_watchdog(self, actuator:     str,
                                   start_time:   str,
                                   end_time:     str, 
                                   time_on:      int,
                                   time_off:     int) -> int:
            
        """
            Function for checking correctness of the data that wants to be inserted.
        """

        # checks if the len of the scring is on accepted len
        if len(actuator) > 60:
            return -1

        # converts the strings to datetime objects to be able to compare them
        try:
            start_time = datetime.strptime(start_time,  '%H:%M:%S')
            end_time   = datetime.strptime(end_time,    '%H:%M:%S')

            if start_time > end_time:
                print("Start time is greater than end time")
                return -1

        except ValueError:
            return -1

        # checks time_on and time_off, negative values
        # mean that the actuator is always on, so 
        # no on-off cycles apply to it.
        
        # it's mandatory for the input values to be both 
        # negative, or both positive, if don't then it's bad input

        if ((time_on < 0) and (time_off > 0)) or ((time_on > 0) and (time_off < 0)):
            return -1

        return 0



    def create_table(self) -> None:
            
        """
            Create the table in the database.
        """

        self.metadata_obj.create_all(self.engine)


    def insert_default_data(self) -> None:

        """
            Inserts default data into the table.
            Mainly used for initialization
        """

        return 0



class Actuators_From_DB(Actuators):

    def __init__(self, engine, table: Table):

        self.engine       = engine
        self.metadata_obj = MetaData()
        self.table        = table
                      
    def create_table(self) -> None:
            
        """
            Create the table in the database.
        """
        print("This table has already been created.")
        return 0


