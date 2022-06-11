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
#print("current working directory: cd .. -> ",  cwd)


from flask import request
from db_mqtt_interface.db.dirty7w7 import *
from db_mqtt_interface.db.db_connection import db_connection
#CONEXIÓN A LA BASE DE DATOS
conn = db_connection(db_host =  db_host,
                     db_name =  db_name,
                     db_user = db_user,
                     db_password =  db_password,
                     db_sslmode = db_sslmode
                    )


#LISTA PARA ALMACENAR EL NOMBRE DE LAS VARIABLES DE ACUERDO A SU 'name' EN LOS DOCUMENTOS .html
simplify_ambiental_variable_names = [   'tome' , 'toma'  ,  'tame' ,  'tama' ,  'taome',
                                        'taoma','taame'  , 'taama' , 'home'  ,  'homa',
                                        'hame' , 'hama'  ,  'eome' ,  'eoma' ,  'eame',
                                        'eama' , 'phome' , 'phoma' , 'phame' , 'phama']


simplify_actuators_variable_names = [   'cada_cuanto', 'duracion_tr','desde_tr',
                                        'hasta_tr'   , 'desde_el'   , 'hasta_el']


ambiental_vars_ = ['temp_optimal', 'temp_ok'   ,'wtemp_optimal', 'wtemp_ok'  , 'hum_optimal',
                   'hum_ok'      , 'ec_optimal',    'ec_ok'    , 'ph_optimal', 'ph_ok']

actuators_vars_ = ['pump', 'lights']

#DICCIONARIO QUE CONTENDRÁ LOS DATOS OPTIMOS Y ACEPTABLES (values -> list) RELACIONADOS A LA LLAVE CUYO NOMBRE ESTARÁ
#RELACIONADO  CON EL NOMBRE DE LAS VARIABLES (keys -> str)
interval_ambiental_vars = {}
interval_actuators_vars = {}




def get_data_from_ambiental_settings(config_: str):

    """
    INPUTS:
            config_: string que indica de qué tabla de las variable ambientales se deben leer los datos,
                     en otras palabras qué configuración sea de 'optimal' o 'ok' va a ser leida y para 
                     qué variable en particular.

    OUTPUTS:
               min_: float tomado de la base de datos
               max_: float tomado de la base de datos  
                     (Son los valores inferior y superior para las condiciones 
                     optimas o aceptables para la variable).
    """ 

    df = conn.read_ambiental_settings(config_= config_)
    min_ = df['min'][0]
    max_ = df['max'][0]    
    return min_, max_

def get_data_from_actuators_settings(config_: str):

    """
    INPUTS:
               config_: string que indica de qué tabla de las variable de los actuadores se deben leer los datos,
                        en otras palabras qué configuración sea de 'pump' o 'lights' va a ser leida

    OUTPUTS:
        Si se quiere la información de 'pump':
               frecuency:  entero que indica la frecuencia con la que se bombeará agua
               duration:   entero que indica la duración del bombeo de agua  
               start_time: hora en la que se debe encender la bomba de agua
               end_time:   hora en la que se debe apagar la bomba de agua

        Si se quiere la información de 'lights':
               start_time: hora en la que se deben encender las luces
               end_time:   hora en la que se deben apagar las luces 
    """

    df = conn.read_actuators_settings(config_ = config_)
    if config_ == 'pump':
        frecuency = df['frequency'][0]
        duration = df['duration'][0]
        start_time = df['start_time'][0]
        end_time = df['end_time'][0]
        return frecuency, duration, start_time, end_time
    
    elif config_ == 'lights':
        start_time = df['start_time'][0]
        end_time = df['end_time'][0]
        return start_time, end_time


#Wrapper function para get_data_from_ambiental_settings()
def get_data_from_all_ambiental_settings(): 
    for variable in ambiental_vars_:
        min_, max_ = get_data_from_ambiental_settings(config_ = variable)
        interval_ambiental_vars[variable] = [min_, max_]


#Wrapper function para get_data_from_actuators_settings()
def get_data_from_all_actuators_settings():
    for variable in actuators_vars_:
        if variable == 'pump':
            frequency, duration, start_time, end_time = get_data_from_actuators_settings(config_=variable)
            interval_actuators_vars[variable] = [frequency,
                                                 duration,
                                                 start_time,
                                                 end_time]
        
        elif variable == 'lights':
            start_time, end_time = get_data_from_actuators_settings(config_=variable)
            interval_actuators_vars[variable] = [start_time, 
                                                 end_time]

def get_info_from_html_form():
    
    """
    Esta función se encarga de hacer un request de la información que se encuentra en
    el formulario html con el fin de poder hacer fill de los campos al hacer cambio de 
    rutas entre 'settings' y 'settings_update'
    (Revisar: 'main_web_huerta.py')
    """

    iterator = 0
    for variable in interval_ambiental_vars.keys():
        interval_ambiental_vars[variable][0] = request.form[simplify_ambiental_variable_names[iterator]]
        interval_ambiental_vars[variable][1] = request.form[simplify_ambiental_variable_names[iterator+1]] 
        iterator+=2
    
    iterator = 0
    for variable in interval_actuators_vars.keys():
        if variable == 'pump':
            interval_actuators_vars[variable][0] = request.form[simplify_actuators_variable_names[iterator]]
            interval_actuators_vars[variable][1] = request.form[simplify_actuators_variable_names[iterator+1]]
            interval_actuators_vars[variable][2] = request.form[simplify_actuators_variable_names[iterator+2]]
            interval_actuators_vars[variable][3] = request.form[simplify_actuators_variable_names[iterator+3]]        
            iterator+=4

        elif variable == 'lights':
            interval_actuators_vars[variable][0] = request.form[simplify_actuators_variable_names[iterator]]
            interval_actuators_vars[variable][1] = request.form[simplify_actuators_variable_names[iterator+1]]


def write_all_ambiental_settings():

    """
    Esta función se encarga de escribir en la base de datos los cambios en los datos de 
    los intervalos de las variables ambientales, hechas por parte del usuario
    """

    for variable in ambiental_vars_:
        conn.write_ambiental_settings(value_min=interval_ambiental_vars[variable][0],
                                      value_max=interval_ambiental_vars[variable][1],
                                      config_= variable)


def write_all_actuators_settings():

    """
    Esta función se encarga de escribir en la base de datos los cambios en los datos de 
    los intervalos de los actuadores, hechas por parte del usuario
    """

    for variable in actuators_vars_:
        if variable == 'pump':
            conn.write_actuators_settings(config_=variable, params=(interval_actuators_vars[variable][2], 
                                                                    interval_actuators_vars[variable][3],
                                                                    interval_actuators_vars[variable][0], 
                                                                    interval_actuators_vars[variable][1]))

        elif variable == 'lights':
            conn.write_actuators_settings(config_='lights', params=(interval_actuators_vars[variable][0],
                                                                    interval_actuators_vars[variable][1]))

