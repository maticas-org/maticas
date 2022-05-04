# necesitamos añadir la carpeta de la clase
# con operaciones sobre la base de datos 
# al path
from sys import path 

# para añadir dicha clase necesitamos saber primero 
# donde estámos parados
from os import getcwd
 
# hago cd .. , para añadir ese path completico
cwd = getcwd()
cwd = cwd.split('/')[:-1]    
cwd = '/'.join(cwd)

# Añade el directorio al path
path.insert(1, cwd) 
print(cwd)

# Importa la clase para hacer operaciones sobre la base de datos
from db_mqtt_interface.db.db_connection import *
from db_mqtt_interface.db.dirty7w7 import *

from db_mqtt_interface.mqtt_python.writeFromMqtt import *
from dirty9w9 import *

# librerías para manejar el tiempo
import datetime
import pytz

import numpy as np 

class daemon:

    """
        Esta clase se encarga de manejar procesos relacionados 
        Con el control de las variables ambientales.

        Se conecta con la base de datos, obtiene información sobre 
        cuales son las condiciones válidas. Y basado en los datos que 
        consulta a la base de datos decide qué hacer para controlar las 
        variables.
    """

    def __init__(self):


        print("Daemon invocado correctamente...")
        print("Ahora las cosas funcionarán mágicamente bien.\n")
        
        print("Conexión a la base de datos...")
        self.db_conn   = db_connection( db_host =  db_host,
                                        db_name =  db_name,
                                        db_user = db_user,
                                        db_password =  db_password,
                                        db_sslmode = db_sslmode)
        print("Correcta.\n")


        # Pone la zona horaria de bogotá colombia
        self.tz = pytz.timezone('America/Bogota')


        #----------------------------------------------------------------------------------
        #              'alias'   |    'nombre del alias         |  'nombre del alias      
        #                        |      de la tabla de          |    de la tabla de       
        #                        |    condiciones optimas       |  condiciones aceptables    
        #                        |  de la variable ambiental    | de la variable ambiental 
        #                        |   mencionada en el alias     |  mencionada en el alias  
        #----------------------------------------------------------------------------------

        self.aliases = {'temp':      ('temp_optimal',               'temp_ok'),
                        'hum':       ('hum_optimal',                'hum_ok'),
                        'lux':       ('lux_optimal',                'lux_ok'),
                        'wtemp':     ('wtemp_optimal',              'wtemp_ok'),
                        'ec':        ('ec_optimal',                 'ec_ok'),
                        'ph':        ('ph_optimal',                 'ph_ok')
                       }

                                    



        print("Conexión al broker MQTT...")
        self.send_conn = mqtt_broker_connection_write( mqtt_broker = mqtt_broker,
                                                       mqtt_port = mqtt_port,
                                                       mqtt_username = mqtt_username,
                                                       mqtt_password = mqtt_password,
                                                       mqtt_client_id = mqtt_client_id 
                                                      )
        print("Correcta.\n")


    def rule_them_all_dady(self):

        colombia_start   = datetime.datetime.now(self.tz)
 
        # Loop
        while True:

            colombia_now = datetime.datetime.now(self.tz)
            delta        = (colombia_now - colombia_start)

            # diferencia de tiempo necesaria para hacer las revisiones
            # las revisiones se hacen cada 5 minutos
            if delta.total_seconds() >= (5*60):

                for alias in self.aliases.keys():
                    print(alias)
                    print(self.check_and_control_variable(alias = alias))

                #reinicia el contador
                colombia_start   = datetime.datetime.now(self.tz)
                print()

    


    def check_and_control_variable(self, alias, variation_threshold = 0):
        
        """
            Revisa y controla la luz, la electroconductividad, el ph, 
            y la temperatura del agua.
        """

        action = self.what_to_do(alias = alias,
                            variation_threshold = variation_threshold)
        
        #######################################################################
        #                   Control de temperatura ambiental 
        #######################################################################

        if alias == 'temp':
            
            # si necesito controlar la temperatura ambiental por 
            # el momento no hay mucho que pueda hacer
            if action == 1:
                return "Por favor aumenta la temperatura ambiental."
                
            elif action == -1:
                return "Por favor disminuye la temperatura ambiental."
                
        #######################################################################
        #                   Control de humedad ambiental 
        #######################################################################

        elif alias == 'hum':
            
            # si necesito controlar la humedad ambiental por 
            # el momento no hay mucho que pueda hacer
            if action == 1:
                return "Por favor aumenta la humedad ambiental."
                
            elif action == -1:
                return "Por favor disminuye la humedad ambiental."

        #######################################################################
        #                   Control de lux ambiental 
        #######################################################################

        elif alias == 'lux':
            
            if action == 1:
                self.send_conn.send_message(alias_topic = 'light', message = '1')
                self.send_conn.send_message(alias_topic = 'light', message = '1')

                
            elif action == -1:
                self.send_conn.send_message(alias_topic = 'light', message = '0')
                self.send_conn.send_message(alias_topic = 'light', message = '0')

        #######################################################################
        #                   Control de  temperatura del agua 
        #######################################################################

        elif alias == 'wtemp':
            
            if action == 1:
                self.send_conn.send_message(alias_topic = 'pump', message = '1')
                self.send_conn.send_message(alias_topic = 'pump', message = '1')

            elif action == -1:
                self.send_conn.send_message(alias_topic = 'pump', message = '0')
                self.send_conn.send_message(alias_topic = 'pump', message = '0')

        #######################################################################
        #                   Control de electroconductividad del agua 
        #######################################################################

        elif alias == 'ec':
            
            #envia 2 veces la orden para asegurarse de que llegue al otro lado
            if action == 1:
                self.send_conn.send_message(alias_topic = 'ec_a', message = '1')
                self.send_conn.send_message(alias_topic = 'ec_a', message = '1')
                time.sleep(3)
                self.send_conn.send_message(alias_topic = 'ec_a', message = '0')
                self.send_conn.send_message(alias_topic = 'ec_a', message = '0')

                self.send_conn.send_message(alias_topic = 'ec_b', message = '1')
                self.send_conn.send_message(alias_topic = 'ec_b', message = '1')
                time.sleep(1.3)
                self.send_conn.send_message(alias_topic = 'ec_b', message = '0')
                self.send_conn.send_message(alias_topic = 'ec_b', message = '0')

            elif action == -1:
                return "Por favor disminuye la electroconductividad del agua."

        #######################################################################
        #                           Control de ph del agua 
        #######################################################################

        elif alias == 'ph':
            
            #envia 2 veces la orden para asegurarse de que llegue al otro lado
            if action == 1:
                self.send_conn.send_message(alias_topic = 'ph_basic', message = '1')
                self.send_conn.send_message(alias_topic = 'ph_basic', message = '1')
                time.sleep(2)
                self.send_conn.send_message(alias_topic = 'ph_basic', message = '0')
                self.send_conn.send_message(alias_topic = 'ph_basic', message = '0')

            elif action == -1:
                self.send_conn.send_message(alias_topic = 'ph_acid', message = '1')
                self.send_conn.send_message(alias_topic = 'ph_acid', message = '1')
                time.sleep(2)
                self.send_conn.send_message(alias_topic = 'ph_acid', message = '0')
                self.send_conn.send_message(alias_topic = 'ph_acid', message = '0')



    def what_to_do(self, alias: str, variation_threshold = 0):

        """
            Revisa como está la variable ambiental y qué se debería hacer.
            
            INPUT:
                    varname     ->  Nombre de la variable que se va a revisar.

            OUTPUT:
                    1, -1, 0    ->  Indica que se debe aumentar el valor  (1).
                                    Indica que se debe disminuir el valor (-1).
                                    No se debe hacer nada (0).
        """

        ok_conditions      = self.db_conn.read_ambiental_settings(config_ = self.aliases[alias][1])
        min_ok             = np.float32(ok_conditions["min"])
        max_ok             = np.float32(ok_conditions["max"])

        direction, value   = self.check_variable_tendence(alias = alias, 
                                                          variation_threshold = variation_threshold)
        
        if value > max_ok:

            return -1

        elif value < min_ok:
        
            return 1

        else:
            return 0


    def check_variable_tendence(self,
                                alias: str,
                                variation_threshold = 0) -> tuple:

        """
            INPUT: 
                    varname     ->  Nombre de la variable que se va a revisar.

            OUTPUT:
                    1, -1, 0    ->  Indica si hay aumento (1).
                                    Si hay decresimiento  (-1).
                                    O si no hay variación fuerte (0).

                    data_mean   ->  media de un 20% de los ultimos datos.

                    la información encunciada anteriormente la retorna en una tupla
                    con este formato:
                    (status, data_mean)
        """

        # timestamp del momento actual en tiempo de colombia
        colombia_now   = datetime.datetime.now(self.tz)
        timestamp_end  = colombia_now.strftime("%Y-%m-%d %H:%M:%S")

        # Mira una hora hacia el pasado 
        # Para revisar los datos y la tendencia que tienen.
        time_diff        = datetime.timedelta(hours=1)
        timestamp_start  = (colombia_now - time_diff).strftime("%Y-%m-%d %H:%M:%S")

        # Consulta a la base de datos 
        data = self.db_conn.read_data(timestamp_end = timestamp_end,
                                      timestamp_start = timestamp_start, 
                                      type_ = alias)

        # Extrae el nombre de la variable consultada en la base de datos
        # esto para poder acceder al campo del dataframe y calcular 
        # su derivada
        varname = self.db_conn.types_dict[alias][1]
        data = np.array(data[varname])

        derivative = data[1:] - data[:-1]

        ndatapoints = derivative.shape[0]
        negative_variation = np.sum(derivative < variation_threshold)
        positive_variation = np.sum(derivative > variation_threshold)

        percentaje_downcrease = negative_variation/ndatapoints
        percentaje_increase   = positive_variation/ndatapoints

        # numero de datos de muestra para calcular la media 
        sample_size = np.ceil(ndatapoints*(0.2)).astype('int32')

        # toma los ultimos "sample_size" datos y calcula una media
        data_mean = np.mean(data[:-sample_size])
        
        # Si la cantidad de datos que van en disminución es mayor al 
        # 60% entonces se considera que se necesita hacer algo
        if percentaje_downcrease > 0.6:
            return (-1, data_mean)

        elif percentaje_increase > 0.6:
            return (1, data_mean)

        else: 
            return (0, data_mean)


    def send_order(self):

        send_conn.send_message(alias_topic = 'light', message = '1')
        send_conn.send_message(alias_topic = 'light', message = '0')
        send_conn.send_message(alias_topic = 'pump', message = '1')
        send_conn.send_message(alias_topic = 'pump', message = '0')



