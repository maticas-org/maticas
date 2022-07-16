from sqlalchemy import MetaData, Table, Column, DateTime, Time, Float, insert, select, delete
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects import postgresql


class Actuator():

    def __init__(self, engine):

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table()

    def insert_data(self, start_time: str, end_time:str) -> int:

        """
        Inserts data into the variable_ok table.
        
        returns 0 if everithing went ok,
                -1 if there was an error.
        """

        if self.insert_data_watchdog(start_time, end_time) == -1:
            return -1

        # statement for insertion of new data
        insert_statement = insert(self.table).values(start_time = start_time, end_time = end_time)
        
        # statement for deletion of previous data
        delete_statement = delete(self.table).where(self.table.c.time <= datetime.utcnow())
        

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


    def insert_data_watchdog(self, start_time: str, end_time: str) -> int:
            
        """
        Function for checking correctness of the data that wants to be inserted.
        """

        # converts the strings to datetime objects to be able to compare them
        start_time = datetime.strptime(start_time, '%H:%M:%S')
        end_time   = datetime.strptime(end_time, '%H:%M:%S')

        if start_time > end_time:
            print("Start time is greater than end time")
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

        self.insert_data(start_time = '06:00:00',
                         end_time   = '19:30:00')


#--------------------------------------------------#
# Defines the classes for the tables based on      #
# the class Actuator.                              #
#--------------------------------------------------#



#------ Lights settings table ------#

class Lights(Actuator):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'lights',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("start_time", Time, nullable = False),
                             Column("end_time", Time, nullable = False))







#------ Water pump settings table ------#

class Water_pump(Actuator):

    #
    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'water_pump',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("frequency", Float(precision = 3), nullable = False),
                             Column("duration", Float(precision = 3), nullable = False),
                             Column("start_time", Time, nullable = False),
                             Column("end_time", Time, nullable = False))

    def insert_data(self, start_time: str, end_time: str, frequency: float, duration: float) -> int:

        """
            inserts configuration instructions into water_pump table

            INPUT:
                    start_time: strings in the format HH:MM:SS, indicates the start time of the water pump
                    end_time:   strings in the format HH:MM:SS, indicates the end time of the water pump
                    frequency:  float, indicates how much time the water pump should be turned off just 
                                after the water has completed a cycle.
                    duration:   float, indicates how long the water pump should be turned on for.
        """

        if self.insert_data_watchdog(start_time, end_time, frequency, duration) == -1:
            return -1

        # statement for insertion of new data
        insert_statement = insert(self.table).values(start_time = start_time,
                                                     end_time   = end_time,
                                                     frequency  = frequency,
                                                     duration   = duration)
        
        # statement for deletion of previous data
        delete_statement = delete(self.table).where(self.table.c.time <= datetime.utcnow())
        

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(delete_statement)
            connection.execute(insert_statement)

        return 0

    def insert_data_watchdog(self,
                             start_time: str,
                             end_time: str,
                             frequency: float,
                             duration: float) -> int:
            
        """
        Function for checking correctness of the data that wants to be inserted.
        """

        # converts the strings to datetime objects to be able to compare them
        start_time = datetime.strptime(start_time, '%H:%M:%S')
        end_time   = datetime.strptime(end_time, '%H:%M:%S')

        if start_time > end_time:
            return -1

        if frequency < 0:
            return -1

        if duration < 0:
            return -1

        return 0

    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(start_time = '06:00:00',
                         end_time   = '20:00:00',
                         frequency  = 40,
                         duration   =  4)
        

