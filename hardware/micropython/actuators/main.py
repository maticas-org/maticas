from actuators_controller import ActuatorsController
from time import sleep 
from json import load


with open("./actuators_config.json") as f:
    config = load(f)

actuators_controller = ActuatorsController(config)

while True:

    actuators_controller.test_actuators()
    sleep(5)
