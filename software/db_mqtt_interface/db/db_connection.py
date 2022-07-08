import datetime
import pytz
import psycopg2
import pandas as pd

class db_connection:

    def __init__(self, db_host, db_name, db_user, db_password, db_sslmode):

        #types_dict: diccionario que hace match entre unos alias cómodos para manejar
        #en el código y los nombres de las variables y tablas en la base de datos

        #-----------------------------------------------------------------------------
        #             'alias' |  'nombre de la tabla' | 'nombre de la var en la tabla'
        #-----------------------------------------------------------------------------
        self.types_dict = {'temp':   ('temperature_',        'temp_level'),
                           'hum':    ('humidity',            'hum_level'),
                           'lux':    ('lux',                 'lux_level'),
                       'pressure':   ('atm_pressure',        'pressure_level'),
                           'wtemp':  ('water_temperature',   'wtemp_level'),
                           'ec':     ('electroconductivity', 'ec_level'),
                           'ph':     ('ph',                  'ph_level')
                          }


        #--------------------------------------------------------------------------------------------------
        #                             'alias'       |  'nombre de la tabla'        | 'nombre de las vars
        #                                           |                              |     en la tabla'
        #--------------------------------------------------------------------------------------------------

        self.ambiental_settings = {'temp_optimal':    ('temperature_optimal',             'min', 'max'),
                                   'temp_ok':         ('temperature_ok',                  'min', 'max'),
                                   'hum_optimal':     ('humidity_optimal',                'min', 'max'),
                                   'hum_ok':          ('humidity_ok',                     'min', 'max'),
                                   'lux_optimal':     ('lux_optimal',                     'min', 'max'),
                                   'lux_ok':          ('lux_ok',                          'min', 'max'),
                                   'ec_optimal':      ('electroconductivity_optimal',     'min', 'max'),
                                   'ec_ok':           ('electroconductivity_ok',          'min', 'max'),
                                   'ph_optimal':      ('ph_optimal',                      'min', 'max'),
                                   'ph_ok':           ('ph_ok',                           'min', 'max'),
                                   'wtemp_optimal':   ('water_temperature_optimal',       'min', 'max'),
                                   'wtemp_ok':        ('water_temperature_ok',            'min', 'max') 
                                 }
                                   

        #--------------------------------------------------------------------------------------------------
        #                             'alias'  |  'nombre de  | 'nombre de las vars
        #                                      |    la tabla' |     en la tabla'
        #--------------------------------------------------------------------------------------------------
        self.actuators_settings = {'pump':      ('water_pump', 'start_time', 'end_time', 'frequency', 'duration'),
                                   'lights':    ('lights',     'start_time', 'end_time')
                                 }
        

        self.tz = pytz.timezone('America/Bogota')

        # Información para conexión con la base de datos 
        self.host = db_host
        self.dbname = db_name
        self.user = db_user 
        self.password = db_password 
        self.sslmode = db_sslmode
        self.default_data_path =  './database_backup_data/'

        # Crea el string de conexión
        self.conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(self.host,
                                                                                          self.user,
                                                                                          self.dbname,
                                                                                          self.password, 
                                                                                          self.sslmode)
        #print(self.conn_string)

        # Activa la conexión con el conn_string
        self.activate_connection()

    def create_tables(self):

        self.conn.set_session(autocommit=True)

        # Crea la base de datos
        self.cursor.execute(open("../../sql/create_variables_tables.sql", "r").read())
        print("DONE sql/create_variables_tables.sql")

        self.cursor.execute(open("../../sql/create_optimal_tables.sql", "r").read())
        print("DONE sql/create_optimal_tables.sql")

        self.cursor.execute(open("../../sql/create_ok_tables.sql", "r").read())
        print("DONE sql/create_ok_tables.sql")

        self.cursor.execute(open("../../sql/create_actuators_tables.sql", "r").read())
        print("DONE sql/create_actuators_tables.sql")

        self.conn.set_session(autocommit=False)




    ###################################################################################
    #        Lectura y escritura en tablas de configuración de las condiciones
    #           optimas o aceptables para algunas variables del cultivo
    ###################################################################################


    def write_ambiental_settings(self, value_min: float,
                                 value_max: float, 
                                 config_: str, 
                                 verbose = False):

        """
        INPUTS:
                value_min: float a ser escrito en la base de datos.
                value_max: float a ser escrito en la base de datos.
                           (Son los valores inferior y superior para las condiciones 
                           optimas o aceptables para la variable).

                config_: string que indica en qué tabla guardar los datos, en otras palabras
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



        # si la config_ ingresada es válida entonces pasa a editar los datos previos
        if config_ in self.ambiental_settings.keys():

            #timestamp: momento de llegada del mensaje de la forma 'YYYY-MM-DD hh:mm:ss'
            colombia_now = datetime.datetime.now(self.tz)
            timestamp = colombia_now.strftime("%Y-%m-%d %H:%M:%S") 

            #nombre de la tabla y de la variable que se va a escribir en esa tabla
            table_name = self.ambiental_settings[config_][0]
            variable_name1 = self.ambiental_settings[config_][1]
            variable_name2 = self.ambiental_settings[config_][2]

            # generación de la query para meter el nuevo dato 
            query = "INSERT INTO {}({}, {}, time) VALUES (%s, %s, %s);".format(table_name,
                                                                               variable_name1,
                                                                               variable_name2)
            # generaciónde la query para borrar el dato viejo
            delete_query = "DELETE FROM {} WHERE time < '{}';".format(table_name, timestamp)

            if verbose:
                print(delete_query)
                print(query)

            self.cursor.execute(delete_query)
            self.cursor.execute(query, (value_min, value_max, timestamp))

            ##
            self.conn.commit()

        else:
            print("bad input")
        


    def read_ambiental_settings(self, config_: str,
                                      verbose = False):

        """
        INPUTS:

                config_: string que indica en qué tabla va a leer los datos.

                         ('temp_optimal',   'temp_ok',      'hum_optimal',  'hum_ok', 
                          'lux_optimal',    'lux_ok',       'ec_optimal',   'ec_ok', 
                          'ph_optimal',     'ph_ok') son una opción.

                verbose: Modo para printear la consulta que se le hace a la base de
                         datos. Principalmente con fines de debugging.
        OUTPUT:
                Retorna un dataframe de pandas con los datos en el intervalo de tiempo seleccionado
                con dos columnas, 'time' y 'variable', donde 'time' es el timestamp del dato.
        """


        #nombre de la tabla y de la variable que se va a escribir en esa tabla
        table_name = self.ambiental_settings[config_][0]
        variable1_name = self.ambiental_settings[config_][1]
        variable2_name = self.ambiental_settings[config_][2]

        query = "select * from {};".format(table_name)

        if verbose:
            print(query)

        #hace la query y la guarda en un dataframe para fácil uso
        data = pd.read_sql(query, self.conn)
        return data



    ###################################################################################
    #        Lectura y escritura en tablas de configuración de las condiciones
    #           optimas o aceptables para algunas variables del cultivo
    ###################################################################################


    def write_actuators_settings(self, config_: str, params: tuple, verbose = False):

        """
            INPUT:
                    config_:    alias para indicar la tabla sobre la que se va a trabajar.
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

        if config_ in self.actuators_settings.keys():

            #timestamp: momento de llegada del mensaje de la forma 'YYYY-MM-DD hh:mm:ss'
            colombia_now = datetime.datetime.now(self.tz)
            timestamp = colombia_now.strftime("%Y-%m-%d %H:%M:%S") 

            #nombre de la tabla y de la variable que se va a escribir en esa tabla
            table_name = self.actuators_settings[config_][0]
            #start_time = self.actuators_settings[type_][1]
            #end_time   = self.actuators_settings[type_][2]


            #generación de la query
            if config_ == 'lights':
                query = "INSERT INTO {}({}, {}, time) VALUES (%s, %s, %s);".format( *self.actuators_settings[config_] )

            else:
                query = "INSERT INTO {}({}, {}, {}, {}, time) VALUES (%s, %s, %s, %s, %s);".format( *self.actuators_settings[config_] )

            # generaciónde la query para borrar el dato viejo
            delete_query = "DELETE FROM {} WHERE time < '{}';".format(table_name, timestamp)

            if verbose:
                print(delete_query)
                print(query)

            self.cursor.execute(delete_query)
            self.cursor.execute(query, (*params, timestamp))

            ##
            self.conn.commit()
            


        else:
            print("bad input")



    def read_actuators_settings(self, config_: str, verbose = False):

        if config_ in self.actuators_settings.keys():

            table_name = self.actuators_settings[config_][0]

            #generación de la query
            query = "SELECT * from  {};".format(table_name)

            if verbose:
                print(query)

            #hace la query y la guarda en un dataframe para fácil uso
            data = pd.read_sql(query, self.conn)

            return data


    ###################################################################################
    #        Lectura y escritura en tablas de datos de variables ambientales
    ###################################################################################


    def write_data(self, value: float, type_: str, verbose = False):

        """
        INPUTS:
                value:      float a ser escrito en la base de datos.

                type_:      string que indica en qué tabla guardar los datos
                            ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph') son una opción.

                verbose:    Modo para printear la consulta que se le hace a la base de
                            datos. Principalmente con fines de debugging.
        OUTPUT:
                None. Esta función escribe los datos en la tabla correspondiente, indicada 
                por la variable 'type_'.
        """

        if type_ in self.types_dict.keys():

            #timestamp: momento de llegada del mensaje de la forma 'YYYY-MM-DD hh:mm:ss'
            colombia_now = datetime.datetime.now(self.tz)
            timestamp = colombia_now.strftime("%Y-%m-%d %H:%M:%S") 

            #nombre de la tabla y de la variable que se va a escribir en esa tabla
            table_name = self.types_dict[type_][0]
            variable_name = self.types_dict[type_][1]

            #generación de la query
            query = "INSERT INTO {}({}, time) VALUES (%s, %s);".format(table_name, variable_name)
            if verbose:
                print(query)

            self.cursor.execute(query, (value, timestamp))

            ##
            self.conn.commit()

        else:
            print("bad input")



    def read_data(self, timestamp_start: str, timestamp_end: str, type_: str, verbose = False):

        """
        INPUTS:
                timestamp_start:    timestamp *desde* donde se quieren seleccionar los datos 
                                    es de la forma -> 'YYYY-MM-DD hh:mm:ss'.
                timestamp_end:      timestamp *hasta* donde se quieren seleccionar los datos 
                                    es de la forma -> 'YYYY-MM-DD hh:mm:ss'.
                
                type_:              llave del diccionario 'self.types_dict' que indica el 
                                    alias de la variable que se quiere consultar.
                                    ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph')
                                    son una opción.
                verbose:            Modo para printear la consulta que se le hace a la base de
                                    datos. Principalmente con fines de debugging.
        OUTPUT:
                Retorna un dataframe de pandas con los datos en el intervalo de tiempo seleccionado
                con dos columnas, 'time' y 'variable', donde 'time' es el timestamp del dato.
        """


        #nombre de la tabla y de la variable que se va a escribir en esa tabla
        table_name = self.types_dict[type_][0]
        variable_name = self.types_dict[type_][1]

        query = "select time, {} from {} \
        where time between '{}' and '{}'".format(variable_name, table_name,
                                                 timestamp_start, timestamp_end)
        if verbose:
            print(query)

        #hace la query y la guarda en un dataframe para fácil uso
        data = pd.read_sql(query, self.conn)
        return data
        



    def activate_connection(self):
        # Crea la conexión

        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()
        print("Connection established")

    def end_connection(self):
        # Acaba todo y cierra la conexión

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def default_table_initialization(self):



        ############################################################
        #          Inicialización por defecto de las tablas
        #                       de settings ambientales
        ############################################################


        #
        self.write_ambiental_settings(  value_min = 15,
                                        value_max = 20,
                                        config_   = 'temp_optimal',
                                      )

        self.write_ambiental_settings(  value_min = 14,
                                        value_max = 24,
                                        config_   = 'temp_ok',
                                      )

        ##
        self.write_ambiental_settings(  value_min = 60,
                                        value_max = 70,
                                        config_   = 'hum_optimal',
                                      )

        self.write_ambiental_settings(  value_min = 50,
                                        value_max = 80,
                                        config_   = 'hum_ok',
                                      )

        ###
        self.write_ambiental_settings(  value_min = 64000,
                                        value_max = 84000,
                                        config_   = 'lux_optimal',
                                      )

        self.write_ambiental_settings(  value_min = 32000,
                                        value_max = 100000,
                                        config_   = 'lux_ok',
                                      )

        ####
        self.write_ambiental_settings(  value_min = 2,
                                        value_max = 2.3,
                                        config_   = 'ec_optimal',
                                      )

        self.write_ambiental_settings(  value_min = 1.8,
                                        value_max = 2.8,
                                        config_   = 'ec_ok',
                                      )

        #####
        self.write_ambiental_settings(  value_min = 5.5,
                                        value_max = 6,
                                        config_   = 'ph_optimal',
                                      )

        self.write_ambiental_settings(  value_min = 5,
                                        value_max = 6.5,
                                        config_   = 'ph_ok',
                                      )

        ######
        self.write_ambiental_settings(  value_min = 10,
                                        value_max = 17,
                                        config_   = 'wtemp_optimal',
                                      )

        self.write_ambiental_settings(  value_min = 8,
                                        value_max = 19,
                                        config_   = 'wtemp_ok',
                                      )

        ############################################################
        #          Inicialización por defecto de las tablas
        #                       de actuadores
        ############################################################

        self.write_actuators_settings(  config_ = 'lights',
                                        params = ('17:00:00', 
                                                  '20:00:00'),
                                      )

        self.write_actuators_settings(config_ = 'pump',
                                      params = ('6:00:00', 
                                                '20:00:00', 
                                                40, 
                                                10)
                                      )

        print("Setting tables initialized.")

        # importa utilidad para descomprimir archivos
        from zipfile import ZipFile

        # usa el hecho de que los alias guardados en las
        # llaves del diccionario son los mismos nombres de los archivos .zip 
        # y de los .csv que contienen, para descomprimir los archivos 
        # y dejarlos en su carpeta correspondiente

        for file in self.types_dict.keys():

            with ZipFile(self.default_data_path + file + '.zip', 'r') as zip_object:
                zip_object.extractall(path = self.default_data_path)

            with open(self.default_data_path + file + '.csv') as csv_file:

                # omite la primera linea que es el encabezado
                csv_file.readline()
                self.cursor.copy_from(  file = csv_file,                  # archivo del cual se va importar a la base 
                                        table = self.types_dict[file][0], # indica el nombre de la tabla
                                        sep=',',
                                        columns = ('time', self.types_dict[file][1]) # especifica el nombre de las columnas
                                      )  
            self.conn.commit()

        print("Data talbles filled with default data.")


    def drop_all_data_tables(self):

        """
            Elimina todas las tablas de datos de variables ambientales 
            de la base de datos. Podría ser útil en casos en que se hayan contaminado
            los datos, o de que se sepa que han sido mal tomados, y se desee hacer
            un reinicio.

            INPUT: None
            OUTPUT: None
        """

        for table in self.types_dict.keys():
            self.cursor.execute("drop table {}".format(self.types_dict[table][0]))
            self.conn.commit()






