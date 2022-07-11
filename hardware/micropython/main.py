from maticas_module1 import Maticas_module1
from time import sleep, ticks_ms

mod = Maticas_module1( ds18b20_pin_number       = 25,
                       ph_pin_number            = 34,
                       ec_signal_pin_number     = 35,
                       ec_power_pin_number      = 32,
                       ec_ground_pin_number     = 33,
                       config_file              = "./mqtt_config.json" )

start_time = ticks_ms()
send_everyn_seconds = 1


send_everyn_mseconds = send_everyn_seconds*1000

while True:

    # once every 10 seconds, it sends the data from the sensors
    if  (ticks_ms() - start_time) > send_everyn_mseconds:

        mod.send_data()
        start_time = ticks_ms()

    mod.mqtt_client.client.check_msg()
    sleep(0.350)
    mod.mqtt_client.client.check_msg()




