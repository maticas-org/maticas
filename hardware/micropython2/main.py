import mqtt_and_module_scheduler as scheduler
import initialize_sensors        as sensors
from json    import load


with open('./mqtt_config.json') as f:
    mqtt_config = load(f)

from mqtt import MqttConnection

mqtt_client = MqttConnection(**mqtt_config)
mqtt_client.mqtt_connect()

sch = scheduler.MQTTModuleScheduler(mqtt_client, sensors.mod)
sch.loop()





