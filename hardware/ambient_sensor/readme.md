# Sensor de variables ambientales

El módulo para medición de variables ambientales es el presentado en este esquema:

<img src="https://github.com/DaveAlsina/maticas/blob/main/hardware/ambient_sensor/imgs/sensor_ambiental_diagrama.png"  height="400">


Como puede notar los sensores usados son el BH1750 y el BME280. El script: *_"./bme280\_and\_BH1750\_2/bme280\_and\_BH1750\_2.ino"_* toma la capacidad de conexión al broker MQTT de hive implementada en *"hardware/hive\_connection"* y le añade la capacidad de enviar los datos de **lux, humedad relativa, temperatura ambiental y presión atmosférica.**



