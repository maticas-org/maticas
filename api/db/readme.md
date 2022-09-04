# Conexión con la base de datos


Los archivos son:

	db_connection.py  dirty7w7.py  main.py

* ***'./db\_connection.py'*** en este archivo se define la clase que hace la conexión a la base de datos postgres en Azure, 
esta clase entre otras cosas cuenta con funcionalidades como:

	* Leer y escribir datos sobre las tablas de la base de datos.
	* Crear las tablas en caso de que no existan.
	* Llenar algunas de estas tablas con datos por defecto una vez creadas las tablas.

* ***'./dirty7w7.py'*** es un archivo que guarda las credenciales para conectase a la base de datos.

* ***'./database\_backup\_data/'*** esta carpeta contiene los comprimidos de los datos que fueron recolectados durante el tiempo 
en que mantuvimos en funcionamiento nuestro sistema de cultivos hidropónico vertical.

* ***'./main.py'*** hace algunas operaciones de lectura y escritura usando la clase definida en ***'./db\_connection.py***, 
su finalidad es principalmente servir como herramienta de chequeos y comprensión de como se interactua con la clase.

Se ejecuta así: 

		python3 ./main.py




