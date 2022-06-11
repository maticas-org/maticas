# Interfaz entre la base de datos y el broker MQTT


Acá se encuentran varios archivos y subcarpetas. A saber:

		db  db_mqtt.py  main_db_mqtt.py  mqtt_python

* ***'db\_mqtt.py'*** contiene la clase que establece una conexión con el broker MQTT y la base de datos. En resumen la clase que allí se define se conecta al broker MQTT, se suscribe a ciertos temas y los escucha, una vez llega un mensaje de alguna variable ambiental se encarga de tomar el mensaje y guardarlo en la base de datos. Usa como template en su construcción al archivo ***'./mqtt\_python/readFromMqtt.py'*** y usa la clase ***'./db/db\_connection.py'*** para guardar los mensajes de variables ambientales en la base de datos.

* El ***'main\_db\_mqtt.py'*** es el archivo que crea una instancia de la clase definida en ***'db\_mqtt.py'***, este archivo debería estar corriendo permanentemente en un computador en la nube ya que sin este los mensajes que se envíen desde los sensores al broker MQTT no serán guardados en la base de datos postgres.

Se ejecuta así *(en caso de que se quiera dejar corriendo permanentemente mientras el computador no se apague)*:

		 nohup python3 ./main_db_mqtt.py &

Para correrlo una sola vez, poder detener el script más fácilmente y ver el output:

		python3 ./main_db_mqtt.py

***Precaución: no corra varios scripts de 'main\_db\_mqtt.py' a la vez ya que podría acabar escribiendo la misma información tantas veces como scripts de 'main\_db\_mqtt.py' tiene corriendo.***


