from sqlalchemy import MetaData, Table, Column, DateTime, Float, String, insert, select, delete, update 
from datetime import datetime
import pandas as pd
from sqlalchemy.dialects import postgresql



"""
+-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
|   time                |   variable      |   min_acceptable   |   max_acceptable    |   min_optimal    |   max_optimal    |
+-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
|                       |                 |                    |                     |                  |                  |
| "YYYY/MM/DD %H:%M:%S" | "variable_name" |       number       |       number        |       number     |       number     |
+-----------------------+-----------------+--------------------+---------------------+------------------+------------------+
"""


class Variable_Intervals():

    def __init__(self,
                 engine,
                 precision = 3):

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table_name = 'variables_intervals'

    def insert_data(self,
                    variable:               str,
                    acceptable_interval:    tuple,
                    optimal_interval:       tuple) -> int:

            """
            Inserts data into the table.
            
                INPUT: 
                        variable:    str with the name of the variable.
                        acceptable_interval: tuple with the acceptable interval. with data type: (float, float).
                                             it has the shape (min_value, max_value).
                        optimal_interval:    tuple with the optimal interval. with data type: (float, float).
                                             it has the shape (min_value, max_value).

                OUTPUT: 0 if everithing went ok,
                        -1 if there was an error.
            """

            if self.insert_data_watchdog(acceptable_interval, optimal_interval) == -1:
                return -1
    
            # Deletes the previous value of the variable if it exists.
            delete_statement = delete(self.table).where(self.table.c.variable == variable)

            # Inserts the value into the table.
            insert_statement = insert(self.table).values(variable = variable,
                                                         min_acceptable = acceptable_interval[0],
                                                         max_acceptable = acceptable_interval[1],
                                                         min_optimal = optimal_interval[0],
                                                         max_optimal = optimal_interval[1])
            

    
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(delete_statement)
                connection.execute(insert_statement)

            return 0


    def read_data(self, variable: str) -> pd.DataFrame:

        """
            Reads data from the table.

            INPUT: None.
            OUTPUT: pandas dataframe with the data.
        """

        statement = select(self.table).where(self.table.c.variable == variable)

        # compiles the statement into a PosgresSQL query string.
        statement = statement.compile(dialect = postgresql.dialect())

        # returns a dataframe with the results
        result = pd.read_sql(statement, self.engine)
        return result

    def insert_data_watchdog(self,
                             acceptable_interval:   tuple,
                             optimal_interval:      tuple) -> int:

        """
            Function for checking correctness of the data that wants to be inserted.

            INPUT: acceptable_interval: tuple with the acceptable interval. with data type: (float, float).
                                        it has the shape (min_value, max_value).

                   optimal_interval:    tuple with the optimal interval. with data type: (float, float).
                                        it has the shape (min_value, max_value).

            OUTPUT: 0 if everithing went ok,
                    -1 if there was an error.
        """

        if acceptable_interval[0] >= acceptable_interval[1]:
            return -1 

        if optimal_interval[0] >= optimal_interval[1]:
            return -1 

        if (acceptable_interval[0] > optimal_interval[0]) or (acceptable_interval[1] < optimal_interval[1]):
            return -1

        return 0 


    def create_table(self) -> None:
            
        """
            Create the table in the database.
        """
        self.table  = Table( self.table_name,
                             self.metadata_obj,       
                             Column("time",           DateTime,             default = datetime.utcnow),
                             Column("variable",       String(60),           primary_key = True),
                             Column("min_acceptable", Float(precision = 3), nullable = False),
                             Column("max_acceptable", Float(precision = 3), nullable = False),
                             Column("min_optimal",    Float(precision = 3), nullable = False),
                             Column("max_optimal",    Float(precision = 3), nullable = False),)

        self.metadata_obj.create_all(self.engine)

    
    def insert_default_data(self) -> None:

        """
            Inserts default data into the table.
            Mainly used for initialization.
        """

        self.insert_data(min_value = 0, max_value = 100)



class Variable_Intervals_From_DB(Variable_Intervals):

    def __init__(self,
                 engine,
                 table: Table):

        self.engine = engine
        self.metadata_obj = MetaData()
        self.table = table

    def create_table(self) -> None:
            
        """
            Create the table in the database.
        """
        print("This table has already been created.")
        return 0




