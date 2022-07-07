import mqtt
from json import load

with open('./mqtt_config.json') as f:
    mqtt_config = load(f)

mqtt_client = MqttConnection(**mqtt_config)

