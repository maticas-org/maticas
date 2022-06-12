# Controlador de bombas peristalticas

El módulo para el control de niveles de electroconductividad y ph, a través de bombas de agua *(adaptable a bombas peristalticas)* es el siguiente:

<p align="center">
<img align = "center" src="https://github.com/DaveAlsina/maticas/blob/main/hardware/peristaltic_pumps_controller/imgs/peristalticas.jpeg"
	 width = "500">
</p>

La idea original fue trabajar con bombas peristalticas para una mejor dosificación sin embargo dados los costos implicados consideramos ir por una solución más económica que resulta menos precisa, el uso de pequeñas bombas de agua de 5V para la regulación de los nutrientes y ph. La forma en que funciona es que hay una cantidad fija de segundos que se deja funcionar la bomba para regular la variable y justo después se enciende la bomba de agua principal del sistema, con la intención de hacer circular la solución nutritiva y que se nivele la concentración de la solución, después de esperar un tiempo prudencial se vuelve a tomar la desición de encender o pagar la bomba de agua reguladora; este proceso de control y regulación se maneja desde el script de la sección de software en **'software/daemon/daemon.py'**.

Tenga en cuenta que todos los módulos usados en esta release de maticas son esp8266.


