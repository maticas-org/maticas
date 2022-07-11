"""

# main used for testing integrated_actuators_mod1 

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
        

"""
# main used for testing integrated_sensors_mod 1

from integrated_sensors_mod1 import integrated_module1
from time import sleep


mod = integrated_module1(   ds18b20_pin_number      = 25,
                            ph_pin_number           = 34,
                            ec_signal_pin_number    = 35,
                            ec_power_pin_number     = 32,
                            ec_ground_pin_number    = 33,
                            mqtt_config_file        = "mqtt_config.json" )
mod.configure_send_data()

while True:

    mod.send_data()
    sleep(1)
"""



