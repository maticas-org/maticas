# Interfaz entre la base de datos y el broker MQTT
----

Acá se encuentran varios archivos y subcarpetas. A saber:

		db  db\_mqtt.py  main\_db\_mqtt.py  mqtt\_python

* ***'db\_mqtt.py'*** contiene la clase que establece una conexión con el broker MQTT y la base de datos. En resumen la clase que allí se define se conecta a al broker MQTT, se suscribe a ciertos temas y los escucha, una vez llega un mensaje de alguna variable ambiental se encarga de tomar el mensaje y guardarlo en la base de datos. Usa como template en su construcción al archivo **'./mqtt\_python/readFromMqtt.py'** y usa la clase **'./db/db\_connection.py'** para guardar los mensajes de variables ambientales en la base de datos.

* El ***'main\_db\_mqtt.py'*** es el archivo que crea una instancia de la clase definida en **'db\_mqtt.py'**, este archivo debería estar corriendo permanentemente en un computador en la nube ya que sin este los mensajes que se envíen desde los sensores al broker MQTT no serán guardados en la base de datos postgres.






