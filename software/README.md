# Maticas

Repositorio de huerta hidropónica automatizada. 
En esta rama trabajamos la sección de ***Software Web*** del proyecto, la estructura de las carpetas es:

* ***sql***, carpeta con las sentencias para crear tablas sql.

* ***db_mqtt_inteface***, Acá se encuentra el script de intersección entre el broker MQTT y la base de datos, así como las clases encargadas de hacer la conexión con la base de datos en postgres y el broker MQTT.

* ***runit.sh***, script que se encarga de correr automáticamente y en el background a los scripts **'./daemon/origami.py'** y
**'./db\_mqtt\_interface/main\_db\_mqtt.py'**, para poder controlar el sistema de una manera inteligente 24/7 y poder guardar los 
datos que llegan de los sensores en la base de datos, respectivamente.







