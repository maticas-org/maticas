from  actuators_controller import ActuatorsController
from mqtt import MqttConnection
from json import load


class integrated_module2():

    def __init__(self, 
                 mqtt_config_file:          str):


        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the MQTT connection
        with open(mqtt_config_file) as f:
            self.mqtt_config = load(f)
 

        # creates de connection object and connects esp32 to the MQTT broker
        self.mqtt_client = MqttConnection(**self.mqtt_config)
        self.mqtt_client.mqtt_connect()


        # creates the actuators controller object
        self.actuators_controller = ActuatorsController(config = self.mqtt_config)

        # rewrites the default callback for the mqtt_client
        self.mqtt_client.client.set_callback(self.control_variable)


    def control_variable(self,
                         topic:   str,
                         msg:     str):

        """
            Wrapper function for controlling a variable given a msg that was recieved 
            on the topic topic.
        """

        topic   = topic.decode('utf-8')
        msg     = msg.decode('utf-8')

        print('Received message {1} on topic: {0}'.format(topic, msg))

        # check if the topic has an alias associated with it
        for alias in self.mqtt_config["sub_topics"]:

            if topic == self.mqtt_config["sub_topics"][alias]["topic"]:
                # if the topic has an alias, then execute the function associated with it
                self.actuators_controller.command_to_variable(variable_alias = alias,
                                                              command        = msg)
                print('Took action \"{0}\" on alias: \"{1}\"'.format(msg, alias))
                break


            
        







