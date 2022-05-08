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
print("current working directory: cd .. -> ",  cwd)

# Importa la clase para hacer operaciones sobre la base de datos
from db_mqtt_interface.db.db_connection import *
from db_mqtt_interface.db.dirty7w7 import *

from db_mqtt_interface.mqtt_python.writeFromMqtt import *
from dirty9w9 import *

# librerías para manejar el tiempo
import datetime
import time
import pytz

# para procesamiento de unos daticos 
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


    def rule_them_all_dady(self, check_everyn_minutes = 5):

        #valores para inicializar el loop
        colombia_start   = datetime.datetime.now(self.tz)

        #valores para inicializar el control de la bomba 
        #de agua en el loop
        current_time_pump = 0
        start_time_pump  = 0 
        finish_time_pump = 0
 
        # Loop
        while True:

            colombia_now = datetime.datetime.now(self.tz)
            delta        = (colombia_now - colombia_start)

            # diferencia de tiempo necesaria para hacer las revisiones
            # las revisiones se hacen cada 5 minutos
            if delta.total_seconds() >= (check_everyn_minutes*60):

                # revisiones y control de las variables ambientales
                for alias in self.aliases.keys():
                    print(alias)
                    print(self.check_and_control_variable(alias = alias))

                #reinicia el contador para determinar cuando 
                #volver a revisar (en check_everyn_minutes minutos)
                colombia_start   = datetime.datetime.now(self.tz)

                # ******************************
                # Control de las luces
                # ******************************
                current_time_light = datetime.datetime.now(self.tz)
                self.control_timed_lights(current_time = current_time_light)

                # ******************************
                # Control de la bomba de agua
                # ******************************

                current_time_pump = datetime.datetime.now(self.tz)

                current_time_pump, start_time_pump, finish_time_pump = self.control_timed_pump(
                                                                            current_time_pump = current_time_pump,
                                                                            start_time_pump   = start_time_pump,
                                                                            end_time_pump     = finish_time_pump )
                print()



            # espera 5 segundos
            time.sleep(5)
    

    #################################################################################
    #                           Controla eventos temporizados
    #                           (cuando encender, apagar luces
    #                                         y
    #                                   bomba de agua)
    #################################################################################


    #################################################################################
    #                           Control de la bomba de agua
    #################################################################################

    def control_timed_pump(self, 
                           current_time_pump: datetime.datetime,
                           start_time_pump:   datetime.datetime,
                           end_time_pump:     datetime.datetime):

        """
            función que revisa si dado un momento de encendido (start_time)
            y un momento de apagado (end_time), y dado un horario fijo 
            en que la bomba puede estar operativa, se debe apagar 
            o encender la bomba de agua.

            INPUT:
                    current_time_pump    -> momento actual
                    start_time_pump      -> momento en que se debería encender la bomba de agua
                    end_time_pump        -> momento en que se debería apagar la bomba de agua
            
            OUTPUT:
                    (current_time_pump, start_time_pump, end_time_pump) actualizados
        """

        code = 'pump'

        # extrae el valor de la hora actual
        current_hour = int(current_time_pump.strftime("%H"))

        # pide las configuraciones de funcionamiento de la bomba de agua
        main_settings = self.db_conn.read_actuators_settings(config_ = code)

        # revisa la hora inicial, desde la que debe encender la bomba
        settings    =  main_settings["start_time"][0]
        settings    =  str(settings)
        start_time  =  datetime.datetime.strptime(settings, "%H:%M:%S")
        start_hour  =  int(start_time.strftime("%H"))

        # revisa la hora final, hasta la que se puede encender la bomba
        settings    =  main_settings["end_time"][0]
        settings    =  str(settings)
        end_time    =  datetime.datetime.strptime(settings, "%H:%M:%S")
        end_hour    =  int(start_time.strftime("%H"))

        # revisa la cantidad de tiempo, que se debe mantener encendida la bomba de agua
        duration    =  int(main_settings["duration"][0])

        # revisa cada cuanto tiempo se debe encender la bomba de agua
        freq        =  int(main_settings["frequency"][0])



        # si esta inicializando entonces manda la orden de encender la bomba
        # (e internamente se revisa si se puede hacer dada la hora)
        if start_time_pump == 0:

            #el momento de incio de la bomba es ahora mismo
            start_time_pump = current_time_pump

            #indica que el momento de finalización es en +duration minutos
            end_time_pump = current_time_pump + datetime.timedelta(minutes = duration)

            # si está en el horario permitido la enciende
            if (current_hour <= end_hour) and (current_hour >= start_hour):

                self.send_conn.send_message(alias_topic = 'pump', message = '1')
                self.send_conn.send_message(alias_topic = 'pump', message = '1')

            # de lo contrario la apaga
            else:

                self.send_conn.send_message(alias_topic = 'pump', message = '0')
                self.send_conn.send_message(alias_topic = 'pump', message = '0')


        # caso en que ya hay inicialización
        else:

            # determina el momento de inicio denuevo basados en 
            # el momento en que se terminó la ejecución + freq min.
            start_time_pump = end_time_pump + datetime.timedelta(minutes = freq)

            # definimos el momento de finalización en caso de que comenzaramos en 
            # start_time_pump (la necesidad de esta variable es que si sobreescribimos
            # end_time_pump el start time se va a poner cada vez más lejos y nunca 
            # encenderíamos la bomba)
            end_time_pump_in_the_future = start_time_pump + datetime.timedelta(minutes = duration)

            # si han pasado freq minutos desde que se apagó la bomba de agua
            # ya es hora de encender la bomba de agua, si y solo si 
            # tengo un momento de finalización que me acota
            if (current_time_pump.timestamp() >= start_time_pump.timestamp() ) and \
               (current_time_pump.timestamp() <= end_time_pump_in_the_future.timestamp() ):

                end_time_pump = end_time_pump_in_the_future

                # si está en el horario permitido la enciende
                if (current_hour <= end_hour) and (current_hour >= start_hour):
                    self.send_conn.send_message(alias_topic = 'pump', message = '1')
                    self.send_conn.send_message(alias_topic = 'pump', message = '1')

                # de lo contrario la apaga
                else:

                    self.send_conn.send_message(alias_topic = 'pump', message = '0')
                    self.send_conn.send_message(alias_topic = 'pump', message = '0')



        return (current_time_pump, start_time, end_time)

    #################################################################################
    #                           Control de las luces
    #################################################################################

    def control_timed_lights(self, 
                             current_time: datetime.datetime):

        """
            Función para encender y apagar la bomba de agua, y las luces
            cuando es necesario.
        """

        code = 'lights'
        current_hour = int(current_time.strftime("%H"))


        main_settings = self.db_conn.read_actuators_settings(config_ = code)

        # revisa la hora final, hasta la que se puede encender la luz
        settings    =  main_settings["end_time"][0]
        settings    =  str(settings)
        end_time    =  datetime.datetime.strptime(settings, "%H:%M:%S")
        end_hour    =  int(end_time.strftime("%H"))

        # revisa la hora inicial, desde la que debe encender la luz
        settings    =  main_settings["start_time"][0]
        settings    =  str(settings)
        start_time  =  datetime.datetime.strptime(settings, "%H:%M:%S")
        start_hour  =  int(start_time.strftime("%H"))
        
        # si está dentro del espacio de tiempo obligatorio 
        # para encender la luz la enciende
        if (current_hour <= end_hour) and (current_hour >= start_hour):
        
            self.send_conn.send_message(alias_topic = 'light', message = '1')
            self.send_conn.send_message(alias_topic = 'light', message = '1')


        #si ya es muy tarde en la noche paga la luz
        elif  (current_hour >= end_hour):

            self.send_conn.send_message(alias_topic = 'light', message = '0')
            self.send_conn.send_message(alias_topic = 'light', message = '0')

        pass

    #################################################################################
    #                   Control de las variables ambientales 
    #                                 por 
    #                                casos 
    #################################################################################

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

            # timestamp del momento actual en tiempo de colombia
            colombia_now   = datetime.datetime.now(self.tz)

            # obtiene la hora en el momento actual
            hour_now  = int(colombia_now.strftime("%H"))

            # revisa la hora final, hasta la que se puede encender la luz
            settings    =  self.db_conn.read_actuators_settings(config_ = 'lights')["end_time"][0]
            settings    =  str(settings)
            end_time    =  datetime.datetime.strptime( settings, "%H:%M:%S" )
            end_hour    =  int(end_time.strftime("%H"))

            
            # si se debe encender y está dentro de los tiempos adecuados entonces bien
            if (action == 1) and (hour_now < end_hour):
                self.send_conn.send_message(alias_topic = 'light', message = '1')
                self.send_conn.send_message(alias_topic = 'light', message = '1')

                
            # si se debe apagar
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

        print(direction, value)
        
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
        print(timestamp_start, timestamp_end)

        # Consulta a la base de datos 
        data = self.db_conn.read_data(timestamp_end = timestamp_end,
                                      timestamp_start = timestamp_start, 
                                      type_ = alias)

        #print(data)

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



