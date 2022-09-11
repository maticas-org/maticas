from json    import load

class Module():

    def __init__(self, 
                 config_file: str):


        # reads the configuration file and stores it in a dictionary
        # for later instantiation of the MQTT connection
        with open(config_file) as f:
            self.mqtt_config = load(f)
 
        self.pub_topics = self.mqtt_config["pub_topics"]
        self.default_initialization()

    
    def default_initialization(self):
        
        """
            Adds the field "exec" to the pub_topics dictionary.
            And sets it's value to "", by default.
        """
        for alias in self.pub_topics.keys():
            self.pub_topics[alias]["exec"] = ""



    ############################################ 
    #        Sampling variables Section        #
    ############################################

    def check_sensors(self) -> None:

        """
            This function checks if all the publish topics 
            have a canditate for requesting measurements.
        """

        for alias in self.pub_topics.keys:

            if "" == self.pub_topics[alias]["exec"]:
                print("topic \"{}\" has no candidate for answering a call".format(alias))
            

    def add_module_function(self,
                            alias: str,
                            function):

        """
            This is the function the user should modify by adding the sensors 
            he/she wants.
        """

        if alias not in self.pub_topics.keys():
            print("this alias does not exist in the pub_topics field. Consider adding it in the file './mqtt_config.json'.")
            return

        self.pub_topics[alias]["exec"] = function
        print("{} added.".format(alias))

        return 0




