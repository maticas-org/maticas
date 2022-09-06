from sqlalchemy import MetaData, Table, Column, DateTime, Float, insert, select, delete
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects import postgresql

# base class to inherit from for the tables
# of optimal interval for values
class Acceptable_interval():

    def __init__(self, engine):

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table()

    def insert_data(self, min_value: float, max_value: float) -> int:

            """
            Inserts data into the variable_ok table.
            
            returns 0 if everithing went ok,
                    -1 if there was an error.
            """

            if self.insert_data_watchdog(min_value, max_value) == -1:
                return -1
    
            # statement for insertion of new data
            insert_statement = insert(self.table).values(min = min_value, max = max_value)
            
            # statement for deletion of previous data
            delete_statement = delete(self.table).where(self.table.c.time <= datetime.utcnow())
            
    
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(delete_statement)
                connection.execute(insert_statement)

            return 0


    def read_data(self):

        """
        Reads data from the humidity_ok table.
        """

        statement = select(self.table)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result


    def insert_data_watchdog(self, min_value: float, max_value: float) -> int:

        """
        Function for checking correctness of the data that wants to be inserted.
        """
        if min_value >= max_value:
            return -1 

        # in this case, given the variables we are controlling 
        # it makes sense not to add negative values to the database.
        if (min_value < 0) or (max_value < 0):
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
        Mainly used for initialization.
        """

        self.insert_data(min_value = 0, max_value = 100)

#----------------------------------------------
# Define classes for the tables in the database
#      here each acceptable interval table is
#      defined as a class which inherits from
#      the base class Acceptable_interval
#----------------------------------------------


#--- Acceptable interval for the Electroconductivity values ---#
class Ec_optimal(Acceptable_interval):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        #This class is used to map the ec table in the database.
        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'electroconductivity_optimal',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("min", Float(precision = 3), nullable = False),
                             Column("max", Float(precision = 3), nullable = False))

    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(min_value = 2, max_value = 2.3)


#--- Acceptable interval for Ph values ---#
class Ph_optimal(Acceptable_interval):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        #This class is used to map the ec table in the database.
        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'ph_optimal',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("min", Float(precision = 3), nullable = False),
                             Column("max", Float(precision = 3), nullable = False))

    def insert_data_watchdog(self, min_value: float, max_value: float) -> int:
        """
        Function for checking correctness of the data that wants to be inserted.
        """
        if min_value >= max_value:
            return -1 

        # in this case, given the variables we are controlling 
        # it makes sense not to add negative values to the database.
        if (min_value < 0) or (max_value < 0):
            return -1

        # how the heck will the ph be more than 14?
        if (min_value > 14) or (max_value > 14):
            return -1

        return 0 

    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(min_value = 6.5, max_value = 6.8)


#--- Acceptable interval for the Humidity values ---#
class Humidity_optimal(Acceptable_interval):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        #This class is used to map the ec table in the database.
        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'humidity_optimal', 
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("min", Float(precision = 2), nullable = False),
                             Column("max", Float(precision = 2), nullable = False))

    def insert_data_watchdog(self, min_value: float, max_value: float) -> int:
        """
        Function for checking correctness of the data that wants to be inserted.
        """
        if min_value > max_value:
            return -1 

        # in this case, given the variables we are controlling 
        # it makes sense not to add negative values to the database.
        if (min_value < 0) or (max_value < 0):
            return -1

        # how the heck will the relative humidity be more than 100%?
        if (min_value > 100) or (max_value > 100):
            return -1

        return 0 

    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(min_value = 60, max_value = 70)




#--- Acceptable interval for the Temperature values ---#
class Temperature_optimal(Acceptable_interval):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        #This class is used to map the ec table in the database.
        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'temperature_optimal',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("min", Float(precision = 2), nullable = False),
                             Column("max", Float(precision = 2), nullable = False))

    def insert_data_watchdog(self, min_value: float, max_value: float) -> int:
        """
        Function for checking correctness of the data that wants to be inserted.
        """
        if min_value > max_value:
            return -1 

        # in this case, given the variables we are controlling 
        # it makes sense not to add negative values to the database.
        if (min_value < 0) or (max_value < 0):
            return -1

        # how the heck will the temperature be more than 100 degrees?
        # indeed forsure more than 60 degrees would kill the plant.
        if (min_value > 100) or (max_value > 100):
            return -1

        return 0 

    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(min_value = 20, max_value = 24)



#--- Acceptable interval for the water temperature values ---#
class Water_temperature_optimal(Acceptable_interval):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        #This class is used to map the ec table in the database.
        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'water_temperature_optimal',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("min", Float(precision = 2), nullable = False),
                             Column("max", Float(precision = 2), nullable = False))

    def insert_data_watchdog(self, min_value: float, max_value: float) -> int:
        """
        Function for checking correctness of the data that wants to be inserted.
        """
        if min_value > max_value:
            return -1 

        # in this case, given the variables we are controlling 
        # it makes sense not to add negative values to the database.
        if (min_value < 0) or (max_value < 0):
            return -1

        # how the heck will the temperature be more than 100 degrees?
        # indeed forsure more than 60 degrees would kill the plant.
        if (min_value > 100) or (max_value > 100):
            return -1

        return 0 


    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(min_value = 15, max_value = 18)



#--- Acceptable interval for the Lux values ---#
class Lux_optimal(Acceptable_interval):

    def __init__(self, engine):

        # inherit methods from Acceptable_interval class
        super().__init__(engine)

        #This class is used to map the ec table in the database.
        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'lux_optimal',
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("min", Float(precision = 2), nullable = False),
                             Column("max", Float(precision = 2), nullable = False))

    def insert_default_data(self) -> None:

        """
        Inserts default data into the table.
        Mainly used for initialization.
        """

        self.insert_data(min_value = 64000, max_value = 84000)


