from ph import Ph
from time import sleep 


ph_sensor = Ph(ph_pin_number = 0)

while True:

    ph = ph_sensor.read_ph()
    print("pH: %.2f" % ph)
    sleep(2)
