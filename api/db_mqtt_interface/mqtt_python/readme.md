# Conexión a broker MQTT


		dirty8w8.py  main_readFromMqtt.py  main_writeFromMqtt.py  readFromMqtt.py  sensor_data.csv  writeFromMqtt.py


* ***'./readFromMqtt.py'***  Define una clase para conectarse al broker MQTT, suscribirse a temas y escuchar los 
mensajes que llegan a estos temas. Se usa para recibir los mensajes que llegan de los sensores.

* ***'./main_readFromMqtt.py'*** Pone a prueba el ***'./readFromMqtt.py'*** con fines también de documentación para 
tener claro también su modo de uso.

* ***'./writeFromMqtt.py'*** Define una clase para conectarse al broker MQTT, suscribirse a temas y escribir en 
estos temas según sea solicitado. Principalmente se usa para controlar los actuadores en el sistema desde la página web.

* ***'./main_writeFromMqtt.py*** Pone a prueba el ***'./writeFromMqtt.py'*** con fines de documentación de igual modo.

* ***'./dirty8w8.py'*** Archivo de credenciales para conectarse al broker (en nuestro caso usamos uno de HiveMQ).

Para ejecutar los mains basta con:

		python3 ./main_readFromMqtt.py

		python3 ./main_writeFromMqtt.py


