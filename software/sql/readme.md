# Creación de las tablas de la base de datos SQL

En esta carpeta se crean las distintas tablas del sistema de cultivos. Esta base de datos es un modelo no relacional, es decir cada 
una de las tablas existe por separado y no tiene relaciones con las demás.


* ***'./create\_variables\_tables.sql'*** crea las tablas correspondientes a las variables ambientales que se van guardando.
* ***'./create\_optimal\_tables.sql'*** crea las tablas que guardan información sobre los niveles mínimos y máximos óptimos
para las variables en que se podría llegar a controlar.
* ***'./create\_ok\_tables.sql'*** crea las tablas que guardan información sobre los niveles mínimos y máximos aceptables
para las variables en que se podría llegar a controlar.

* ***'./create\_actuators\_tables.sql'***, crea tablas que guardan las configuraciones de funcionamiento de los actuadores (luces y bomba de agua).

Imagen de las tablas de variables y sus niveles optimos en su esquema
---------------------------------------------------------------------

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/sql/imgs/variables_and_optimals.png"
	 width = "500" >
</p>

Imagen de las tablas de niveles aceptables y las configuraciones de las luces y la bomba de agua
-------------------------------------------------------------------------------------------------

<p align="center">
<img align="center" src="https://github.com/DaveAlsina/maticas/blob/main/software/sql/imgs/oks_and_actuators.png"
	 width = "500" >
</p>

Tenga en cuenta que esto es solo para crear las tablas de la base de datos, usted aún debe crear la base de datos, y el usuario dave 
para poder crear las tablas.






