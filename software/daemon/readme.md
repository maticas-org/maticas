# Control del sistema de cultivos

En esta carpeta se hace el demonio del sistema o en otras palabras el espíritu del sistema, lo que le da vida, en ***./daemon.py*** 
se hace el control del sistema de cultivos basandose en las mediciones que van llegando del cultivo. En ***./origami.py*** se
pone a correr la clase controladora desarrollada en ***./daemon.py***. En ***./dirty9w9.py*** se añaden las credenciales para
conectarse al broker MQTT.

Este script debe estar corriendo 24/7 para un correcto crecimiento de las plantas.

