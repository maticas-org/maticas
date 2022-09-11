from mqtt import MqttConnection
from json import load

with open('./mqtt_config.json') as f:
    mqtt_config = load(f)

mqtt_client = MqttConnection(**mqtt_config)

# connects esp32 to the internet 
mqtt_client.start_internet_connection()


