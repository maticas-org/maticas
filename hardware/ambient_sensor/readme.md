# Sensor de variables ambientales

El módulo para medición de variables ambientales es el presentado en este esquema:

![Diagrama de conexiones de los sensores del módulo de medición ambiental][./imgs/sensor\_ambiental\_diagrama.png]

Como puede notar los sensores usados son el BH1750 y el BME280. El script: *_"./bme280\_and\_BH1750\_2/bme280\_and\_BH1750\_2.ino"_* toma la capacidad de conexión al broker MQTT de hive implementada en *"hardware/hive\_connection"* y le añade la capacidad de enviar los datos de **lux, humedad relativa, temperatura ambiental y presión atmosférica.**



