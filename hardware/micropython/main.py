from integrated_sensors_mod1 import integrated_module1
from time import sleep


integrated_module1(ds18b20_pin_number = 32,
                   mqtt_config_file = "mqtt_config.json")

while True:

    integrated_module1.send_data()
    sleep(1)



