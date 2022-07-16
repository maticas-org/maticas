import datetime
import pytz
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

from sys import path
from os.path import abspath, dirname

# the directory where the database is defined to the path
current_file_directory = dirname(abspath(__file__))
database_definition_directory = "/define_db"
path.append(current_file_directory + database_definition_directory )

# imports database tables definitions 
from ambiental_variables import *
from acceptable_values_intervals import *
from optimal_values_intervals import *
from actuators_settings import *

class DbConnection():

    #-----------------------------------------------#
    # Initialization and configuration of the class #
    #-----------------------------------------------#

    def __init__(self, 
                 db_host: str,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_sslmode: str ):

        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_sslmode = db_sslmode

        conn_string = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
        #print(conn_string)

        self.engine = create_engine(conn_string)
        self.configure_connection()
            

    def configure_connection(self) -> None:

        """
            This function is intended to be easily modified by the user if desired, 
            here you specify the aliases for the tables that will be used for the 
            database.
        """

        self.tables = {"ec":        Ec(engine = self.engine), 
                       "ph":        Ph(engine = self.engine), 
                       "hum":       Humidity(engine = self.engine),
                       "temp":      Temperature_(engine = self.engine),
                       "wtemp":     Water_temperature(engine = self.engine),
                       "lux":       Lux(engine = self.engine),
                       "pressure":  Atm_pressure(engine = self.engine)}

        self.tables_ok = {"hum_ok":     Humidity_ok(engine = self.engine),
                          "temp_ok":    Temperature_ok(engine = self.engine),
                          "wtemp_ok":   Water_temperature_ok(engine = self.engine),
                          "ec_ok":      Ec_ok(engine = self.engine),
                          "ph_ok":      Ph_ok(engine = self.engine),
                          "lux_ok":     Lux_ok(engine = self.engine)}
 
        self.tables_optimal = {"hum_optimal":     Humidity_optimal(engine = self.engine),
                               "temp_optimal":    Temperature_optimal(engine = self.engine),
                               "wtemp_optimal":   Water_temperature_optimal(engine = self.engine),
                               "ec_optimal":      Ec_optimal(engine = self.engine),
                               "ph_optimal":      Ph_optimal(engine = self.engine),
                               "lux_optimal":     Lux_optimal(engine = self.engine)}

        self.tables_actuators = {"pump": Water_pump(engine = self.engine),
                                 "lights": Lights(engine = self.engine)}

        print("Done setting up the configuration.")

    def create_tables(self) -> None:

        """
        Create the tables in the database.
        """

        for table in self.tables.values():
            table.create_table()
        print("Done creating ambiental variable tables.")

        for table_ok in self.tables_ok.values():
            table_ok.create_table()
        print("Done creating acceptable values tables.")

        for table_optimal in self.tables_optimal.values():
            table_optimal.create_table()
        print("Done creating optimal values tables.")

        for table_actuator in self.tables_actuators.values():
            table_actuator.create_table()
        print("Done creating actuators settings tables.")

        print("-"*60)


    def insert_default_data(self) -> None:

        """
        This function inserts the default values for the acceptable and optimal values.
        """

        for table_ok in self.tables_ok.values():
            table_ok.insert_default_data()
        print("Done inserting default values in acceptable values tables.")


        for table_optimal in self.tables_optimal.values():
            table_optimal.insert_default_data()
        print("Done inserting default values in optimal values tables.")


        for table_actuator in self.tables_actuators.values():
            table_actuator.insert_default_data()
        print("Done inserting default values in actuators settings tables.")


        # uses the fact that the default zipped data has the pattern in their names:
        # default_alias.zip and inside the zip the file is called default_alias.csv
        for alias, table in self.tables.items():
            table.insert_default_data(data_file_name = alias)

        print("Done inserting default values in ambiental variable tables.")
        print("-"*60)

    ############################################################# 
    #-----------------------------------------------------------#
    # Functions to read and write the ambiental variable tables #
    #-----------------------------------------------------------#


    def write_data(self, value: float, alias: str, verbose = False) -> None:

        """
        INPUTS:
                value:      float to be written in the database.

                alias:      nickname to indicate the table where the data will be written. and inside the zip the file is called wq
                            ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph') are the default options.
                            You can change that inside the function 'self.configure_connection'.

                verbose:    Option to show the output/status of the query.
                            Exit code 0, means no problem and -1 means there was a problem.
        OUTPUT:
                None. This function writes the data in the table corresponding to the alias.
        """

        if alias not in self.tables.keys():
            print("Not existent table: {}".format(alias))
            return 

        result = self.tables[alias].insert_data(value = value)

        if verbose:
            print("Inserted data in table {0}, with exit code: {1}".format(alias, result))


    def read_data(self, timestamp_start: str, timestamp_end: str, alias: str) -> pd.DataFrame:

        """
        INPUTS:
                timestamp_start:    Start timestamp of the data to be read. It's format is 
                                    'YYYY-MM-DD HH:MM:SS'.
                timestamp_end:      End timestamp of the data to be read. It's format is
                                    'YYYY-MM-DD HH:MM:SS'.

                alias:              nickname to indicate the table where the data will be read.
                                    This nickname is selected in the function 'self.configure_connection'.
                                    the default options of aliases for ambiental variables are:
                                    ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph').
                                    
                                    If you need to make any changes to the aliases, refer to that function.
                
        OUTPUT:
                Returns a pandas dataframe with two columns, 'time' and 'variable', where 'time' is the
                timestamp of the data, and 'variable' contains the data associated to the alias in the
                timestamp. (Notice 'variable' won't be the name of the column, it's just a general name format, 
                to explain the output data).
        """

        if alias not in self.tables.keys():
            print("Not existent table: {}".format(alias))
            return

        return self.tables[alias].read_data(timestamp_start = timestamp_start,
                                            timestamp_end = timestamp_end)

    ############################################################# 
    #-----------------------------------------------------------#
    # Functions to read and write the ambiental settings, it is #
    # the acceptable and optimal intervals definition for each  #
    # ambiental variable where it is important to know.         #
    #-----------------------------------------------------------#

    def write_ambiental_settings(self, 
                                 min_value: float,
                                 max_value: float, 
                                 alias: str, 
                                 verbose = False) -> None:

        """
        INPUTS:
                alias:  nickname to indicate the table where the data will be written.
                        It could be an optimal value table or an acceptable value table.
                        Options for the default aliases are:

                         ('temp_optimal',   'temp_ok',      'hum_optimal',  'hum_ok', 
                          'lux_optimal',    'lux_ok',       'ec_optimal',   'ec_ok', 
                          'ph_optimal',     'ph_ok',        'wtemp_ok',     'wtemp_optimal').
                

                value_min: minimum acceptable or optimal value for the variable.
                value_max: maximum acceptable or optimal value for the variable.

                verbose:   Mainly for debugging purposes.
        OUTPUT:
                None. This function writes the data in the table corresponding to the alias.
        """

        if alias  in self.tables_ok.keys():
            result = self.tables_ok[alias].insert_data(min_value = min_value, max_value = max_value)

        elif alias in self.tables_optimal.keys():
            result = self.tables_optimal[alias].insert_data(min_value = min_value, max_value = max_value)

        else:
            print("Not existent table: {}".format(alias))
            return


        if verbose:
            print("Inserted data in table {0}, with exit code: {1}".format(alias, result))


    def read_ambiental_settings(self, alias: str) -> pd.DataFrame:

        """
        INPUTS:

                alias: Indicates the table where the data will be read. Default aliases are:

                         ('temp_optimal',   'temp_ok',      'hum_optimal',  'hum_ok', 
                          'lux_optimal',    'lux_ok',       'ec_optimal',   'ec_ok', 
                          'ph_optimal',     'ph_ok',        'wtemp_ok',     'wtemp_optimal').

        OUTPUT:
                Returns a pandas dataframe with three columns, 'min', 'max' and 'time', where 'min' is the
                minimum acceptable or optimal value for the variable, and 'max' is the maximum acceptable or
                optimal value for the variable. 'time' is the timestamp of when that setting was set.
        """

        if alias  in self.tables_ok.keys():
            data = self.tables_ok[alias].read_data()

        elif alias in self.tables_optimal.keys():
            data = self.tables_optimal[alias].read_data()

        else:
            print("Not existent table: {}".format(alias))
            return


        return data

    ############################################################# 
    #-----------------------------------------------------------#
    # Functions to read and write the actuators settings, it is #
    # the definition of when an actuator starts working and     #
    # when it stops working. And if necessary the time it rests,#
    # and the time it works.                                    #
    #-----------------------------------------------------------#


    def write_actuators_settings(self, alias: str, params: dict, verbose = False):

        """
            INPUT:
                    alias:      nickname to indicate the table where the data will be written.
                                Remember that the default options for the aliases are:
                                ('pump', 'lights'), these are defined in the function 'self.configure_connection'.

                                If you need to make any changes to the aliases, refer to that function.

                    params:     dictionary with the parameters to be written in the table.
                                params could be a dictionary with this structure if you want to write to the water_pump:
                                {'start_time':  'HH:MM:SS', 
                                 'end_time':    'HH:MM:SS', 
                                 'frequency':    float (indicating minutes),
                                 'duration':     float (indicating minutes)}

                                if you want to write to the lights:
                                {'start_time':  'HH:MM:SS',
                                 'end_time':    'HH:MM:SS'}

                    verbose:    Mainly for debugging purposes.

            OUTPUT:
                    None. This function writes the data in the table corresponding to the alias.
        """

        if alias in self.tables_actuators.keys():
            result = self.tables_actuators[alias].insert_data(**params)

        else:
            print("Not existent table: {}".format(alias))
            return

        if verbose:
            print("Inserted data in table {0}, with exit code: {1}".format(alias, result))
        

    def read_actuators_settings(self, alias: str) -> pd.DataFrame:

        """
            INPUT:
                    alias:      nickname to indicate the table where the data will be written.
                                Remember that the default options for the aliases are:
                                ('pump', 'lights'), these are defined in the function 'self.configure_connection'.

                                If you need to make any changes to the aliases, refer to that function.

            OUTPUT:
                    Returns a pandas dataframe with five columns, 'start_time', 'end_time', 'frequency', 'duration' and 'time',
                    where 'start_time' is the time when the actuator will start, 'end_time' is the time when the actuator will stop,
                    'frequency' is the time in minutes that the actuator "rests", and 'duration' is the time in minutes that 
                    the actuator will be active. 'time' is the timestamp of when that setting was set. (this is the output when 
                    alias is 'pump'). 

                    When the alias is 'lights', the output is a dataframe with three columns, 'start_time', 'end_time' and 'time'.
                    With same meaning as in the previous case.
        """

        if alias not in self.tables_actuators.keys():
            return

        return self.tables_actuators[alias].read_data()





