# Maticas

Repositorio de huerta hidropónica automatizada. 
En esta rama trabajamos la sección de hardware del proyecto, la estructura de las carpetas es:

* ambient\_sensor, aquí se trabajan los sensores BH1750 y BME280 para enviar lecturas de lux, temperatura ambiental
presión atmosférica, humedad relativa y presión atmosférica.

* ec\_sensor, en esta carpeta se usa la sonda ds18b20 junto con unas resistencias y un cable para hacer un sensor 
de electroconductividad en el agua.

* ph\_sensor, contiene el código de manejo del sensor de ph y envío de mediciones de esta variable.

* peristaltic\_pump, esta carpeta está destinada al código que se encarga del manejo de 4 bombas peristálticas para la 
regulación del ph.

* pump\_controller, es la carpeta de código para controlar la bomba que circula en agua por todo el sistema.





