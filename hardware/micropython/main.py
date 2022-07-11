from integrated_actuators_mod1 import integrated_module2
from time import sleep

mod = integrated_module2(mqtt_config_file = "./mqtt_config.json")

while True:

    try:
        mod.mqtt_client.client.check_msg()

    except OSError:
        print("MQTT connection lost. Reconnecting...")
        mod.mqtt_client.restart_and_reconnect()
        

"""
from integrated_sensors_mod1 import integrated_module1
from time import sleep


mod = integrated_module1(   ds18b20_pin_number  = 32,
                            ph_pin_number       = 33,
                            mqtt_config_file    = "mqtt_config.json" )
mod.configure_send_data()

while True:

    mod.send_data()
    sleep(1)
"""



