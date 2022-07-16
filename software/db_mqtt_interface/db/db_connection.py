import datetime
import pytz
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

from define_db.ambiental_variables import *
from define_db.acceptable_values_intervals import *
from define_db.optimal_values_intervals import *
from define_db.actuators_settings import *

class DbConnection():

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
            
        pass

    def configure_connection(self):

        """
            This function is intended to be easily modified by the user if desired, 
            here you specify the aliases for the tables that will be used for the 
            database.
        """

        self.tables = {"ec":        Ec(engine = self.engine), 
                       "ph":        Ph(engine = self.engine), 
                       "temp":      Temperature_(engine = self.engine),
                       "wtemp":     Water_temperature(engine = self.engine),
                       "lux":       Lux(engine = self.engine),
                       "pressure":  Atm_pressure(engine = self.engine)}

        self.tables_ok = {"hum_ok":     Humidity_ok(engine = self.engine),
                          "temp_ok":    Temperature_ok(engine = self.engine),
                          "ec_ok":      Ec_ok(engine = self.engine),
                          "ph_ok":      Ph_ok(engine = self.engine),
                          "lux_ok":     Lux_ok(engine = self.engine)}
 
        self.tables_optimal = {"hum_optimal":     Humidity_optimal(engine = self.engine),
                               "temp_optimal":    Temperature_optimal(engine = self.engine),
                               "ec_optimal":      Ec_optimal(engine = self.engine),
                               "ph_optimal":      Ph_optimal(engine = self.engine),
                               "lux_optimal":     Lux_optimal(engine = self.engine)}

        self.tables_actuators = {"pump": Water_pump(engine = self.engine),
                                 "lights": Lights(engine = self.engine)}


    def create_tables(self):
        """
        Create the tables in the database.
        """

        for table in self.tables.values():
            table.create_table()

        for table_ok in self.tables_ok.values():
            table_ok.create_table()


    ######################################################################
    ######################################################################


    def write_data(self, value: float, alias: str, verbose = False) -> None:

        """
        INPUTS:
                value:      float to be written in the database.

                alias:      nickname to indicate the table where the data will be written.
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



    def read_data(self, timestamp_start: str, timestamp_end: str, alias: str, verbose = False) -> pd.DataFrame:

        """
        INPUTS:
                timestamp_start:    timestamp *desde* donde se quieren seleccionar los datos 
                                    es de la forma -> 'YYYY-MM-DD hh:mm:ss'.
                timestamp_end:      timestamp *hasta* donde se quieren seleccionar los datos 
                                    es de la forma -> 'YYYY-MM-DD hh:mm:ss'.
                
                alias:              llave del diccionario 'self.tables' que indica el 
                                    alias de la variable que se quiere consultar.
                                    ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph')
                                    son una opción.
                verbose:            Modo para printear la consulta que se le hace a la base de
                                    datos. Principalmente con fines de debugging.
        OUTPUT:
                Retorna un dataframe de pandas con los datos en el intervalo de tiempo seleccionado
                con dos columnas, 'time' y 'variable', donde 'time' es el timestamp del dato.
        """

        if alias not in self.tables.keys():
            print("Not existent table: {}".format(alias))
            return

        return self.tables[alias].read_data(timestamp_start = timestamp_start,
                                            timestamp_end = timestamp_end)


    def write_ambiental_settings(self, 
                                 min_value: float,
                                 max_value: float, 
                                 alias: str, 
                                 verbose = False) -> None:

        """
        INPUTS:
                value_min: float a ser escrito en la base de datos.
                value_max: float a ser escrito en la base de datos.
                           (Son los valores inferior y superior para las condiciones 
                           optimas o aceptables para la variable).

                alias: string que indica en qué tabla guardar los datos, en otras palabras
                         qué configuración sea de 'optimal' o 'ok' va a ser modificada 
                         y para qué variable en particular.

                         ('temp_optimal',   'temp_ok',      'hum_optimal',  'hum_ok', 
                          'lux_optimal',    'lux_ok',       'ec_optimal',   'ec_ok', 
                          'ph_optimal',     'ph_ok') son una opción.

                verbose:    Modo para printear la consulta que se le hace a la base de
                            datos. Principalmente con fines de debugging.
        OUTPUT:
                None. Esta función escribe los datos en la tabla correspondiente, indicada 
                por la variable 'config_' y su diccionario 'self.ambiental_settings'.

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


    def read_ambiental_settings(self, alias: str,
                                      verbose = False) -> pd.DataFrame:

        """
        INPUTS:

                alias: string que indica en qué tabla va a leer los datos.

                         ('temp_optimal',   'temp_ok',      'hum_optimal',  'hum_ok', 
                          'lux_optimal',    'lux_ok',       'ec_optimal',   'ec_ok', 
                          'ph_optimal',     'ph_ok') son una opción.

                verbose: Modo para printear la consulta que se le hace a la base de
                         datos. Principalmente con fines de debugging.
        OUTPUT:
                Retorna un dataframe de pandas con los datos en el intervalo de tiempo seleccionado
                con dos columnas, 'time' y 'variable', donde 'time' es el timestamp del dato.
        """

        if alias  in self.tables_ok.keys():
            data = self.tables_ok[alias].read_data()

        elif alias in self.tables_optimal.keys():
            data = self.tables_optimal[alias].read_data()

        else:
            print("Not existent table: {}".format(alias))
            return

        if verbose:
            print("Read data from table {0}".format(alias))

        return data

    ######################################################################
    ######################################################################

    def write_actuators_settings(self, alias: str, params: tuple, verbose = False):

        """
            INPUT:
                    alias:      alias para indicar la tabla sobre la que se va a trabajar.
                                Recuerde que los alias se definen en 'self.actuators_settings'.
                                Las opciones son -> ('pump', 'lights').
                    params:     tupla que contiene todos los parámetros que se van a escribir.
                                deben ser en el orden en que especifica el valor correspondiente
                                a la llave 'config_' del diccionario 'self.actuators_settings'.
                                Observe como el nombre de la tabla no se debe incluir dentro de 
                                params.
                                
                                Es decir params deben ser:
                                ('start_time', 'end_time', 'frequency', 'duration') ó 
                                ('start_time', 'end_time')
                    verbose:    Modo para printear la consulta que se le hace a la base de
                                datos. Principalmente con fines de debugging.
            OUTPUT:
        """

        if alias in self.tables_actuators.keys():
            result = self.tables_actuators[alias].insert_data(**params)

        else:
            print("Not existent table: {}".format(alias))
            return

        if verbose:
            print("Inserted data in table {0}, with exit code: {1}".format(alias, result))
        

    def read_actuators_settings(self,
                                alias: str,
                                verbose = False):

        if alias not in self.tables_actuators.keys():
            return


        data = self.tables_actuators[alias].read_data()
        return data





