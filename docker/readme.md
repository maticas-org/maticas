# Maticas Docker App

Una documentación completa de como usar el docker container para hostear la base de datos y el broker 
en un solo contenedor se encuentra [acá](https://hub.docker.com/r/dleyvacastro/maticas) (aún no usamos docker compose).

sobre los scripts que se encuentran en esta carpeta:

* ***./docker\_start*** Script para empezar a correr el docker.
* ***./passcript.py*** Script para crear y borrar usuarios del broker mosquitto que corre en el docker container.
* ***./mosquitto.conf*** configuraciones por defecto para el mosquitto (supondré que si quieres cambiar algo acá sabes lo que haces).




