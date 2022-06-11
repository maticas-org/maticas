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
import schedule

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

        ####################################################
        #   diccionarios para guardar las configuraciones 
        ####################################################

        #             |||       Configuración               ||| cada cuantos
        #             |||                                   ||| minutos se actualiza    
        #             |||                                   ||| o se ejecuta la función
        #-----------------------------------------------------------------------
        self.timing_settings = {'update_pump_settings'          :       60, 
                                'update_lights_settings'        :       50, 
                                'control_timed_pump'            :       -1, 
                                'control_timed_lights'          :       5,
                                'check_and_control_variables'   :       10}


        #             |||       Configuración               ||| valor por defecto previo 
        #             |||                                   ||| a la inicialización   
        #-----------------------------------------------------------------------
        self.pump_settings  = { 'start_hour'                            : -1, 
                                'end_hour'                              : -1,
                                'duration'                              : -1, 
                                'freq'                                  : -1,
                                'proportion'                            : -1,
                                'check_every_n_minutes'                 : -1}

        self.light_settings = { 'start_hour'                            : -1, 
                                'end_hour'                              : -1}


        #inicializa los diccionarios
        self.update_pump_settings()
        self.update_lights_settings()

        #####################################################################
        # Definición de variables usadas frecuentemente para correr 
        #               eventos o controlar actuadores
        #####################################################################

        self.iteration_count_pump = 0.0



    def rule_them_all_dady(self):

        # eventos de actualización de configuraciones
        schedule.every(self.timing_settings['update_pump_settings']).minutes.do(self.update_pump_settings)
        schedule.every(self.timing_settings['update_lights_settings']).minutes.do(self.update_lights_settings)

        # eventos de control
        schedule.every(self.timing_settings['control_timed_lights']).minutes.do(self.control_timed_lights)
        schedule.every(self.timing_settings['control_timed_pump']).minutes.do(self.control_timed_pump)
        schedule.every(self.timing_settings['check_and_control_variables']).minutes.do(self.check_and_control_variables)



        # Loop
        while True:

            schedule.run_pending()

            # espera 1 segundos
            time.sleep(1)
    

    #################################################################################
    #                       Actualiza los diccionarios que guardan 
    #                   Las configuraciones que pueden estar cambiando 
    #                               por solicitud del usuario
    #################################################################################

    def update_lights_settings(self):

        """
        INPUT:
                None.

        OUTPUT: None.

            Actualiza la información de los diccionarios que guardan las configuraciones
            de las luces.
        """

        code = 'lights'
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

        self.light_settings['start_hour']   = start_hour
        self.light_settings['end_hour']     = end_hour

        print("Light settings were updated: ")
        print(self.light_settings)
        print("----"*100)

    def update_pump_settings(self):

        """
        INPUT:
                None.

        OUTPUT: None.

            Actualiza la información de los diccionarios que guardan las configuraciones
            de la bomba de agua.
        """

        code = 'pump'

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
        end_hour    =  int(end_time.strftime("%H"))

        # revisa la cantidad de tiempo, que se debe mantener encendida la bomba de agua
        duration    =  int(main_settings["duration"][0])

        # revisa cada cuanto tiempo se debe encender la bomba de agua
        freq        =  int(main_settings["frequency"][0])

        # actualiza las configuraciones 
        self.pump_settings['start_hour']             = start_hour
        self.pump_settings['end_hour']               = end_hour 
        self.pump_settings['duration']               = duration
        self.pump_settings['freq']                   = freq 
        self.pump_settings['proportion']             = min(freq, duration)/(duration + freq)
        self.pump_settings['check_every_n_minutes']  = min(freq, duration)

        # sobreescribe la configuración de cada cuanto revisar si se debe apagar o no la bomba
        # de agua
        self.timing_settings['control_timed_pump'] = self.pump_settings['check_every_n_minutes']

        print("Pump settings were updated: ")
        print(self.pump_settings)
        print("----"*100)

    #################################################################################
    #                           Controla eventos temporizados
    #                           (cuando encender, apagar luces
    #                                         y
    #                                   bomba de agua)
    #################################################################################

    #################################################################################
    #                           Control de la bomba de agua
    #################################################################################

    def control_timed_pump(self):

        """
            Funció que revisa si según el horario es hora de encender 
            o apagar la bomba de agua.

            INPUT:
                    None.
            
            OUTPUT:
                    None.
        """

        # hora actual en colombia, o en el timezone seleccionado
        current_time = datetime.datetime.now(self.tz)
        current_hour = int(current_time.strftime("%H"))
        
        # si es muy tarde se debe apagar la bomba 
        if (current_hour > self.pump_settings['end_hour']):

            print("Very late {} h, pump is off".format(current_hour) )

            self.send_order( alias = 'pump',
                            message = '0',
                            resend_times = 5,
                            starting_delay = 0.1,
                            step_size = 0.085 )

            return 

        # si es muy temprano se debe apagar la bomba también
        if (current_hour < self.pump_settings['start_hour']):
                 
            print("Very early {} h, pump is off".format(current_hour) )
            self.send_order( alias = 'pump',
                            message = '0',
                            resend_times = 5,
                            starting_delay = 0.1,
                            step_size = 0.085 )

            return 

        # la función que queremos replicar es:
        #  
        #      
        #   |  
        # 1 |-----          -----            -----           
        #   |                                                 
        # 0 |     ----------      ----------       ----------
        #  _____________________________________
        #   |
        #   |
        
        # note que esto se compone de una unica oscilación que se repite:
        #   |  
        # 1 |-----          
        #   |               
        # 0 |     ----------
        #  _____________________________________
        #   |
        #   |

        # --> esta tiene un periodo: [tiempo_encendido + tiempo_apagado]
        # si medimos la parte del periodo en la que estamos inicio (0)
        # o fin (1) podemos determinar cuando encender la bomba

        # inicialización del contador 
        # counter = 0.0

        # cada cuanto tiempo se va a tomar la decisión de encende o apagar:
        # tiempo_minimo = min(tiempo_apagado, tiempo_encendido)

        # aumento del contador con el tiempo 
        # counter += [tiempo_minimo]/[tiempo_apagado + tiempo_encendido]

        ######################
        # si no es obligatorio apagar la bomba entonces 
        # se debe encender la bomba y revisar si es momento para ello 
        ######################

        # está inicializando, está empezando la 'oscilación'
        # y esta es como medio 'coseno' empieza encendido un ratito 
        # después se apaga un rato más largo, y  repite
        if (self.iteration_count_pump == 0.0):


            self.send_order( alias = 'pump',
                             message = '1',
                             resend_times = 10,
                             starting_delay = 0.1,
                             step_size = 0.05 )

            self.iteration_count_pump += self.pump_settings['proportion'] 
            print("Initialization {} h, pump is on".format(current_hour) )


        # si ya completó la oscilación entonces es un 1 
        # y se debe resetear ese contador 
        elif (self.iteration_count_pump > 1.0):

            self.send_order( alias = 'pump',
                             message = '1',
                             resend_times = 5,
                             starting_delay = 0.1,
                             step_size = 0.085 )

            #resetea el contador a: (0 + [tiempo_minimo]/[tiempo_apagado + tiempo_encendido] 
            self.iteration_count_pump = self.pump_settings['proportion'] 
            print("Recovery period completed {} h, pump is on".format(current_hour) )


        # si aún no ha completado la oscilación aumente el contador y 
        # mantenga apagada la bomba de agua
        else:

            self.send_order( alias = 'pump',
                             message = '0',
                             resend_times = 5,
                             starting_delay = 0.1,
                             step_size = 0.085 )

            self.iteration_count_pump += self.pump_settings['proportion'] 
            print("Recovery period {} h, pump is off. Period is: {}".format(current_hour,
                                                                            self.iteration_count_pump) )


        return 



    #################################################################################
    #                           Control de las luces
    #################################################################################

    def control_timed_lights(self):

        """
            Función para encender y apagar las luces
            cuando es necesario según el horario.
        """

        # hora actual en colombia, o en el timezone seleccionado
        current_time = datetime.datetime.now(self.tz)
        current_hour = int(current_time.strftime("%H"))

        # si es muy tarde se debe apagar la luz
        if (current_hour > self.light_settings['end_hour']):

            print("Very late {} h, light is off".format(current_hour) )
            self.send_order( alias = 'light',
                             message = '0',
                             resend_times = 5,
                             starting_delay = 0.1,
                             step_size = 0.085 )
            return

        # si es muy temprano se debe apagar la bomba también
        if (current_hour < self.light_settings['start_hour']):
                 
            print("Very early {} h, light is off".format(current_hour) )
            self.send_order( alias = 'light',
                             message = '0',
                             resend_times = 5,
                             starting_delay = 0.1,
                             step_size = 0.085 )

            return


        print("Just in time for schedule {} h, light is on".format(current_hour) )
        self.send_order(alias = 'light',
                        message = '1',
                        resend_times = 5,
                        starting_delay = 0.1,
                        step_size = 0.1)



    #################################################################################
    #                   Control de las variables ambientales 
    #                                 por 
    #                                casos 
    #################################################################################

    def check_and_control_variables(self):

        for var in self.aliases.keys():

            self.check_and_control_variable(alias = var)


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

            # si se debe encender y esta dentro de los tiempos adecuados entonces bien
            if (action == 1) and (hour_now <= self.light_settings['end_hour']) and \
               (hour_now >= self.light_settings['start_hour']):

                self.send_order(alias = 'light',
                                message = '1',
                                resend_times = 4,
                                starting_delay = 0.1,
                                step_size = 0.1)

                
            # si se debe apagar
            elif action == -1:
                self.send_order(alias = 'light',
                                message = '0',
                                resend_times = 4,
                                starting_delay = 0.1,
                                step_size = 0.1)


        #######################################################################
        #                   Control de  temperatura del agua 
        #######################################################################

        elif alias == 'wtemp':
            
            if action == 1:
                self.send_order(alias = 'pump',
                                message = '1',
                                resend_times = 4,
                                starting_delay = 0.1,
                                step_size = 0.1)

            elif action == -1:
                self.send_order(alias = 'pump',
                                message = '0',
                                resend_times = 4,
                                starting_delay = 0.1,
                                step_size = 0.1)

        #######################################################################
        #                   Control de electroconductividad del agua 
        #######################################################################

        elif alias == 'ec':
            
            #envia 2 veces la orden para asegurarse de que llegue al otro lado
            if action == 1:

                #########
                # enciende la bomba de ec a y la apaga después
                # de un rato
                #########

                self.send_order(alias = 'ec_a',
                                message = '1',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)

                time.sleep(4)

                self.send_order(alias = 'ec_a',
                                message = '0',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)

                #########
                # enciende la bomba de ec b y la apaga después
                # de un rato
                #########

                self.send_order(alias = 'ec_b',
                                message = '1',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)

                time.sleep(2)

                self.send_order(alias = 'ec_b',
                                message = '0',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)

            elif action == -1:
                return "Por favor disminuye la electroconductividad del agua."

        #######################################################################
        #                           Control de ph del agua 
        #######################################################################

        elif alias == 'ph':
            
            #envia 2 veces la orden para asegurarse de que llegue al otro lado
            if action == 1:

                #########
                # apaga y enciende la bomba de ph basic
                #########
                self.send_order(alias = 'ph_basic',
                                message = '1',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)

                time.sleep(3)

                self.send_order(alias = 'ph_basic',
                                message = '0',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)


            elif action == -1:

                #########
                # apaga y enciende la bomba de ph acid
                #########
                self.send_order(alias = 'ph_acid',
                                message = '1',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)

                time.sleep(3)

                self.send_order(alias = 'ph_acid',
                                message = '0',
                                resend_times = 10,
                                starting_delay = 0.1,
                                step_size = 0.05)



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


    def send_order(self,
                   alias: str,
                   message: int,
                   resend_times = 4,
                   starting_delay = 0.1,
                   step_size = 0.1):

        """
            INPUT: 
                    alias           ->   Identificador de el tema al que se va a escribir
                                          ( la lista de aliases está en: 
                                            db_mqtt_interface.mqtt_python.writeFromMqtt ).

                    message         ->  '1' ó '0' para encender o apagar los dispositivos 
                                         a los que se comunica con el alias.  

                    resend_times    ->  Número de veces que se va a reenviar el mensaje 
                                        (el módulo arduino no soporta QoS 2 entonces para
                                         compensar se hace retransmisión automática del mensaje).

                    starting_delay  ->  Para no saturar el broker o los microcontroladores 
                                        y dar tiempo de reacción al broker entonces manda mensajes 
                                        cada cierto tiempo determinado por esta variable.

                    step_size       ->  El tiempo de espera para retransmitir el mensaje aumenta cada 
                                        que se envía, y este aumento está determinado por esta variable.

            OUTPUT:

                    None.
        """

        for i in range(resend_times - 1):
            # envía el mensaje al tema 
            self.send_conn.send_message(alias_topic = alias,
                                        message = message)

            # espera un momento para hacer la retransmisión del mensaje
            time.sleep(starting_delay)

            # aumenta el tiempo de espera para retransmitir los próximos
            # mensajes 
            starting_delay += step_size

        #envía el último mensaje 
        self.send_conn.send_message(alias_topic = alias,
                                    message = message)



