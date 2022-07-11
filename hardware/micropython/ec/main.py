from ec import Ec
from time import sleep

ec_sensor = Ec(ec_signal_pin_number     = 35,
               ec_power_pin_number      = 32,
               ec_ground_pin_number     = 33)


while True:

    ec = ec_sensor.read_ec(wtemperatue = 20)
    print("EC: {}".format(ec))
    sleep(5)

