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
        

    def write_data(self, value: float, type_: str, verbose = False):

        """
            value: float a ser escrito en la base de datos.
            type_: string que indica en qué tabla guardar los datos
                   ('temp', 'hum', 'lux', 'press', 'wtemp', 'ec', 'ph') son una opción.
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

