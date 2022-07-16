from sqlalchemy import MetaData, Table, Column, DateTime, Float, insert, select, delete
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects import postgresql


# -------------------------------------------
#   base class to inherit repetitive methods
#   to other variables.
# -------------------------------------------

class Variable():

    def __init__(self, engine):

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table = Table()

    def read_data(self, timestamp_start, timestamp_end)-> pd.DataFrame:

        """
        Reads data from the ec table, between the 
        specified timestamps.
        """

        statement = select(self.table).\
                    where(self.table.c.time >= timestamp_start).\
                    where(self.table.c.time <= timestamp_end)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)

        return result

    def create_table() -> None:
            
        """
        Create the table in the database.
        """
        metadata_obj.create_all(self.engine)



#---------------------------------------------------------#
#         Declaring classes for tables                    #
#            and operations on them                       #
#---------------------------------------------------------#


#- Electroconductivity  table-#

class Ec(Variable):

    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table = Table( 'electroconductivity', 
                            self.metadata_obj,
                            Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                            Column("ec_level", Float(precision = 3), nullable   = False) )

    def insert_data(self, value: float) -> None:

        """
        Inserts data into the ec table.
        """

        statement = insert(self.table).values(ec_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)



#- Ph table -#

class Ph(Variable):

    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'ph', 
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("ph_level", Float(precision = 3), nullable   = False) )


    def insert_data(self, value: float) -> int:

        """
        Inserts data into the ph table.

        if any error with the data it returns -1, 
        if a successfully inserted data it returns 0.
        """

        if (value < 0) or (value > 14):
            return -1

        statement = insert(self.table).values(ph_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0


class Temperature_(Variable):
    
    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)


        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'temperature_', 
                            self.metadata_obj,
                            Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                            Column("temp_level", Float(precision = 2), nullable   = False) )


    def insert_data(self, value: float) -> int:

        """
        Inserts data into the ph table.

        if any error with the data it returns -1, 
        if a successfully inserted data it returns 0.
        """

        if value < 0:
            return -1

        statement = insert(self.table).values(temp_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0


#- water_temperature table -#

class Water_temperature(Variable):

    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'water_temperature', 
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("wtemp_level", Float(precision = 2), nullable   = False) )


    def insert_data(self, value: float) -> int:

        """
        Inserts data into the ph table.

        if any error with the data it returns -1, 
        if a successfully inserted data it returns 0.
        """

        if value < 0:
            return -1

        statement = insert(self.table).values(wtemp_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0


#- humidity table -#
class Humidity(Variable):

    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'humidity', 
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("hum_level", Float(precision = 2), nullable   = False) )


    def insert_data(self, value: float) -> int:

        """
        Inserts data into the ph table.

        if any error with the data it returns -1, 
        if a successfully inserted data it returns 0.
        """

        if value < 0:
            return -1

        statement = insert(self.table).values(hum_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0


#- lux table -#
class Lux(Variable):

    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'lux', 
                             self.metadata_obj,
                             Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                             Column("lux_level", Float(precision = 2), nullable   = False) )


    def insert_data(self, value: float) -> int:

        """
        Inserts data into the ph table.

        if any error with the data it returns -1, 
        if a successfully inserted data it returns 0.
        """

        if value < 0:
            return -1

        statement = insert(self.table).values(lux_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0


class Atm_pressure(Variable):
    
    def __init__(self, engine):

        # inherit methods from Variable class
        # particularly the read_data method
        super().__init__(engine)

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table  = Table( 'atm_pressure', 
                            self.metadata_obj,
                            Column("time", DateTime, primary_key = True, default = datetime.utcnow),
                            Column("pressure_level", Float(precision = 2), nullable   = False) )


    def insert_data(self, value: float) -> int:

        """
        Inserts data into the ph table.

        if any error with the data it returns -1, 
        if a successfully inserted data it returns 0.
        """

        if value < 0:
            return -1

        statement = insert(self.table).values(pressure_level = value)

        with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(statement)

        return 0



