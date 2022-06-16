# Aplicación Web 

Acá hicimos la contrucción de la página web en flask combinando partes con dash. La página depende de los siguientes elementos para funcionar: 

* Conexión a la base de datos postgres hosteada en servicios de Microsoft Azure (No necesariamente debe ser Azure, pero si se quiere usar exactamente el mismo código sin necesidad de hacer muchos cambios Azure es una buena opción).

* Conexión al broker MQTT HiveMQ, ya que hay botones que envían órdenes a los módulos de control en el sistema de cultivo.

Sobre los archivos que vemos acontinuación:

* ***'./data\_dash\_app.py'*** allí se desarrolla la página de visualización de los datos que van llegando a la base de datos.
* ***'./detailed_data_dash_app.py'*** contiene el código para la visualización de un análisis un poco más detallado sobre las variables
medidas.
* ***'./manipulate_data_for_settings.py'*** desarrolla la de modificación de campos del form inicial que se ve en la página de settings.
* ***'./main_web_huerta.py'***, renderiza todas las ventanas y corre la página web, si se quisiera iniciar esta página web este sería 
el script que se debería correr.
* ***'./templates/'***, contiene la definición de la estructura de la página de settings en HTML.
* ***'./static/'***, se compone de constantes css.


Vista de página de configuración de la huerta
--------------------------------------------------------

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/settings_parte1.png"
	 width = "500" >
</p>
<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/settings_parte2.png"
	 width = "500" >
</p>



Vista de página de visualización de datos de la huerta
--------------------------------------------------------

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/data_parte1.png"
	 width = "500" >
</p>

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/data_parte2.png"
	 width = "500" >
</p>

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/data_parte3.png"
	 width = "500" >
</p>



Vista de página de análisis extra
-------------------------------------------------------

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/detailed_analisys_parte1.png"
	 width = "500" >
</p>

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/app_web/imgs/detailed_analisys_parte2.png"
	 width = "500" >
</p>




