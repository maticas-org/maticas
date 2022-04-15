import datetime
import psycopg2
import pandas as pd

class db_connection:

    def __init__(self, db_host, db_name, db_user, db_password, db_sslmode):

        #types_dict: diccionario que hace match entre unos alias cómodos para manejar
        #en el código y los nombres de las variables y tablas en la base de datos

        #-----------------------------------------------------------------------------
        #             'alias' |  'nombre de la tabla' | 'nombre de la var en la tabla'
        #-----------------------------------------------------------------------------
        self.types_dict = {'temp':   ('temperature',         'temp_level'),
                           'hum':    ('humidity',            'hum_level'),
                           'lux':    ('lux',                 'lux_level'),
                       'pressure':   ('atm_pressure',        'pressure_level'),
                           'wtemp':  ('water_temperature',   'wtemp_level'),
                           'ec':     ('electroconductivity', 'ec_level'),
                           'ph':     ('ph',                  'ph_level')
                          }

        # Información para conexión con la base de datos 
        self.host = db_host
        self.dbname = db_name
        self.user = db_user 
        self.password = db_password 
        self.sslmode = db_sslmode

        # Crea el string de conexión
        self.conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(self.host,
                                                                                          self.user,
                                                                                          self.dbname,
                                                                                          self.password, 
                                                                                          self.sslmode)
        print(self.conn_string)

        # Activa la conexión con el conn_string
        self.activate_connection()

    def create_tables(self):

        # Crea la base de datos
        
        ###########################################################################
        #                       Tablas de variables del cultivo 
        ###########################################################################

        #cursor.execute("DROP DATABASE IF EXISTS sensors_data;")
        #cursor.execute("CREATE DATABASE sensors_data;")
        #print("Finished creating database")

        #crea la tabla de temperature
        #-- object: public.temperature | type: TABLE --
        #-- DROP TABLE IF EXISTS public.temperature CASCADE;
        self.cursor.execute('CREATE TABLE IF NOT EXISTS                  \
                                    public.temperature (                \
                                    temp_level float4 NOT NULL,         \
                                    "time" timestamp NOT NULL,          \
                                    CONSTRAINT temperature_pk PRIMARY KEY ("time"));\
                            ALTER TABLE public.temperature OWNER TO dave;')

        print("Finished creating table *temperature*")

        #crea la tabla de humidity
        #-- object: public.humidity | type: TABLE --
        #-- DROP TABLE IF EXISTS public.humidity CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS              \
                                    public.humidity (               \
                                    hum_level float4 NOT NULL,      \
                                    "time" timestamp NOT NULL,      \
                                    CONSTRAINT humidity_pk PRIMARY KEY ("time") ); \
                            ALTER TABLE public.humidity OWNER TO dave;')
        
        print("Finished creating table *humidity*")

        #crea la tabla de temperature del agua 
        #-- object: public.water_temperature | type: TABLE --
        #-- DROP TABLE IF EXISTS public.water_temperature CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS              \
                            public.water_temperature (              \
                                    wtemp_level float8 NOT NULL,    \
                                    "time" timestamp NOT NULL,      \
                                    CONSTRAINT water_temperature_pk PRIMARY KEY ("time") ); \
                            ALTER TABLE public.water_temperature OWNER TO dave;')
        
        print("Finished creating table *water_temperature*")

        #crea la tabla de electroconductivity 
        #-- object: public.electroconductivity | type: TABLE --
        #-- DROP TABLE IF EXISTS public.electroconductivity CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS              \
                            public.electroconductivity (            \
                                ec_level float4 NOT NULL,           \
                                "time" timestamp NOT NULL,          \
                                CONSTRAINT electroconductivity_pk PRIMARY KEY ("time")); \
                            ALTER TABLE public.electroconductivity OWNER TO dave;')
        
        print("Finished creating table *electroconductivity*")


        #crea la tabla de electroconductivity 
        #-- object: public.ph | type: TABLE --
        #-- DROP TABLE IF EXISTS public.ph CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS      \
                            public.ph (                     \
                                ph_level float4 NOT NULL,   \
                                "time" timestamp NOT NULL,  \
                                CONSTRAINT ph_pk PRIMARY KEY ("time")); \
                            ALTER TABLE public.ph OWNER TO dave;')
        
        print("Finished creating table *ph*")

        
        #crea la tabla de lux 
        #-- object: public.lux | type: TABLE --
        #-- DROP TABLE IF EXISTS public.lux CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS      \
                            public.lux (                    \
                                lux_level float8 NOT NULL,  \
                                "time" timestamp NOT NULL,  \
                                CONSTRAINT lux_pk PRIMARY KEY ("time")); \
                            ALTER TABLE public.lux OWNER TO dave;')
        
        print("Finished creating table *lux*")


        #crea la tabla de atm_pressure 
        #-- object: public.atm_pressure | type: TABLE --
        #-- DROP TABLE IF EXISTS public.atm_pressure CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS              \
                        public.atm_pressure (                   \
                            pressure_level float4 NOT NULL,     \
                            "time" timestamp NOT NULL,          \
                            CONSTRAINT atm_pressure_pk PRIMARY KEY ("time")); \
                        ALTER TABLE public.atm_pressure OWNER TO dave;')
        
        print("Finished creating table *atm_pressure*")
        
        ###########################################################################
        #                           Tablas de optimal settings
        ###########################################################################

        #crea la tabla de optimal_humidity 
        #-- object: public.optimal_humidity | type: TABLE --
        #-- DROP TABLE IF EXISTS public.optimal_humidity CASCADE;    

        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.optimal_humidity(                                \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT optimal_humidity PRIMARY KEY ("time"));  \
                            ALTER TABLE public.optimal_humidity OWNER TO dave;')
        
        print("Finished creating table *optimal_humidity*")


        #crea la tabla de optimal_temperature 
        #-- object: public.optimal_temperature  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.optimal_temperature CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                                 \
                            public.optimal_temperature(                                 \
                                "time" timestamp NOT NULL,                              \
                                min float4 NOT NULL,                                    \
                                max float4 NOT NULL,                                    \
                                CONSTRAINT optimal_temperature PRIMARY KEY ("time"));   \
                            ALTER TABLE public.optimal_temperature OWNER TO dave;')

        print("Finished creating table *optimal_temperature*")
        
        #crea la tabla de optimal_ph 
        #-- object: public.optimal_ph  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.optimal_ph CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.optimal_ph(                                      \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT optimal_ph PRIMARY KEY ("time"));        \
                            ALTER TABLE public.optimal_ph OWNER TO dave;')

        print("Finished creating table *optimal_ph*")



        #crea la tabla de optimal_ec 
        #-- object: public.optimal_ec  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.optimal_ec CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.optimal_ec(                                      \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT optimal_ec PRIMARY KEY ("time"));        \
                            ALTER TABLE public.optimal_ec OWNER TO dave;')

        print("Finished creating table *optimal_ec*")


        #crea la tabla de optimal_lux 
        #-- object: public.optimal_lux  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.optimal_lux CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.optimal_lux(                                     \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT optimal_lux PRIMARY KEY ("time"));       \
                            ALTER TABLE public.optimal_lux OWNER TO dave;')

        print("Finished creating table *optimal_lux*")


        ###########################################################################
        #                           Tablas de ok settings
        ###########################################################################

        #crea la tabla de ok_humidity 
        #-- object: public.ok_humidity  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.ok_humidity CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.ok_humidity(                                     \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT ok_humidity PRIMARY KEY ("time"));       \
                            ALTER TABLE public.ok_humidity OWNER TO dave;')

        print("Finished creating table *ok_humidity*")


        #crea la tabla de ok_temperature 
        #-- object: public.ok_temperature  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.ok_temperature CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.ok_temperature(                                     \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT ok_temperature PRIMARY KEY ("time"));       \
                            ALTER TABLE public.ok_temperature OWNER TO dave;')

        print("Finished creating table *ok_temperature*")


        #crea la tabla de ok_ph 
        #-- object: public.ok_ph  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.ok_ph CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.ok_ph(                                     \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT ok_ph PRIMARY KEY ("time"));       \
                            ALTER TABLE public.ok_ph OWNER TO dave;')

        print("Finished creating table *ok_ph*")


        #crea la tabla de ok_ec 
        #-- object: public.ok_ec  | type: TABLE --
        #-- DROP TABLE IF EXISTS public.ok_ec CASCADE;    
        self.cursor.execute('CREATE TABLE if NOT EXISTS                             \
                            public.ok_ec(                                     \
                                "time" timestamp NOT NULL,                          \
                                min float4 NOT NULL,                                \
                                max float4 NOT NULL,                                \
                                CONSTRAINT ok_ec PRIMARY KEY ("time"));       \
                            ALTER TABLE public.ok_ec OWNER TO dave;')

        print("Finished creating table *ok_ec*")





    def write_data(self, value: float, type_: str, verbose = False):

        """
        INPUTS:
                value: float a ser escrito en la base de datos.
                type_: string que indica en qué tabla guardar los datos
                       ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph') son una opción.

        OUTPUT:
                None. Esta función escribe los datos en la tabla correspondiente, indicada 
                por la variable 'type_'.
        """


        if type_ in self.types_dict.keys():

            #timestamp: momento de llegada del mensaje de la forma 'YYYY-MM-DD hh:mm:ss'
            timestamp = datetime.datetime.now()

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













"""
cursor.execute("DROP TABLE IF EXISTS public.temperatura CASCADE;")
cursor.execute("DROP TABLE IF EXISTS public.temperatura_agua CASCADE;")
cursor.execute("DROP TABLE IF EXISTS public.humedad CASCADE;")
cursor.execute("DROP TABLE IF EXISTS public.lux CASCADE;")
cursor.execute("DROP TABLE IF EXISTS public.ph CASCADE;")
cursor.execute("DROP TABLE IF EXISTS public.electroconductivity CASCADE;")
cursor.execute("DROP TABLE IF EXISTS public.presion_atm CASCADE;")
"""

"""
def write_test_data():

    #print("escribiendo data...")

    for t in types_dict.keys():
        write_data(value = 6.6 , type_ = t)
        read_data(timestamp_start = '2020-01-01 00:00:00', timestamp_end = '2023-01-01 00:00:00', type_ = t)

    #print("data escrita!")

"""

