from  actuators_controller import ActuatorsController
from mqtt import MqttConnection

from ds18b20 import ds18b20
from ph import Ph
from ec import Ec
from json import load

class Maticas_module1():

    
    def __init__(self, 
                 config_file: str,
                 ds18b20_pin_number: int,
                 ph_pin_number:int,
                 ec_signal_pin_number:int,
                 ec_power_pin_number: int,
                 ec_ground_pin_number: int):


        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the MQTT connection
        with open(config_file) as f:
            self.mqtt_config = load(f)
 

        # creates de connection object and connects esp32 to the MQTT broker
        self.mqtt_client = MqttConnection(**self.mqtt_config)
        self.mqtt_client.mqtt_connect()


        # rewrites the default callback for the mqtt_client
        self.mqtt_client.client.set_callback(self.control_variable)

        # creates the actuators controller object
        self.actuators_controller = ActuatorsController(config = self.mqtt_config)

        # creates the ds18b20 object with the given pin_number 
        self.ds18b20 = ds18b20(pin_number = ds18b20_pin_number)

        # creates the ph sensor object with the given pin_number
        self.ph     = Ph(pin_number = ph_pin_number)

        # creates the ec sensor object with the given pins numbers
        self.ec     = Ec(  ec_signal_pin_number     = ec_signal_pin_number,
                           ec_power_pin_number      = ec_power_pin_number,
                           ec_ground_pin_number     = ec_ground_pin_number)

        # configures the MQTT client to publish the data from the added sensors
        # if you want to add more sensors, just add them to the 'pub_topics'
        # field in the 'mqtt_config.json' file and then add here an instance of 
        # the sensor object. Don't forget to modify the configure_send_data function
        # by adding something like:

        # self.mqtt_client.pub_topics["your_variable_alias"]["exec"] = self.your_sensor_instance.read_your_Variable
        self.configure_send_data()

    ##################################
    #        Control Section         #
    ##################################

    def control_variable(self,
                         topic:   str,
                         msg:     str):

        """
            Wrapper function for controlling a variable given a msg that was recieved 
            on the topic topic.
        """

        # decodes the incomig information because it's in bytes format
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

    ############################################ 
    #        Sampling vaiables Section         #
    ############################################

    def read_ec_wrapper(self):

        """
            This function is a wrapper for the ec sensor object.
            It returns the data from the ec sensor.
        """

        # gets the water temperature from the ds18b20 sensor
        temp = self.mqtt_client.pub_topics["wtemp"]["exec"]()

        # provides the water temperature to the ec sensor
        # to return the measurement
        return self.ec.read_ec(wtemperature = temp)

    def configure_send_data(self):

        """
            This function configures the MQTT client to publish the data from the
            selected sensors, using a simple sintaxis:

            self.mqtt_client.pub_topics[alias]["exec"] = function_to_be_executed

            were the function_to_be_executed is a function that returns the data
            from the sensor.
        """

        self.mqtt_client.pub_topics["wtemp"]["exec"] = self.ds18b20.read_temperature 
        self.mqtt_client.pub_topics["ec"]["exec"]    = self.read_ec_wrapper
        self.mqtt_client.pub_topics["ph"]["exec"]    = self.ph.read_ph 


    def send_data(self):

        """
            This function sends data to all the topics that exist in the 'pub_topics'
            field from the 'mqtt_config.json' file.

            Its mandatory for the dictionary 'self.mqtt_client.pub_topics' to have 
            the following structure:

            {
                "alias": { "exec": function_to_be_executed,
                           "topic": topic_to_be_published, 
                           "qos": qos_to_be_used
                         },
                        
                        ...
 
                "alias": { "exec": function_to_be_executed,
                           "topic": topic_to_be_published, 
                           "qos": qos_to_be_used
                         }
            }

            if no "exec" field is present with correspondig function_to_be_executed,
            no data will be sent tho that topic.

        """

        for alias in self.mqtt_client.pub_topics.keys():

            if "exec" in self.mqtt_client.pub_topics[alias].keys():

                # executes the function that returns the data from the sensor
                data = self.mqtt_client.pub_topics[alias]["exec"]()
                print("sending data from {0}, value: {1}".format(alias, data))

                self.mqtt_client.publish( topic = self.mqtt_client.pub_topics[alias]["topic"],
                                          msg   = str(data),
                                          qos   = self.mqtt_client.pub_topics[alias]["qos"]     )

                #check if any incoming message was recived while taking 
                #the data from the sensor
                self.mqtt_client.client.check_msg()

        print("-"*10)

