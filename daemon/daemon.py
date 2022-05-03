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
from db_mqtt_interface.mqtt_python.dirty8w8 import *



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
        print("Ahora las cosas funcionarán mágicamente bien.")
        









