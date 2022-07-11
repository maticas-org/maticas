from machine import Pin
from time import sleep

class ActuatorsController():


    """
        This class defines some pins, and sets them as output, and on
        request turns them on and off.
         in maticas it's used on esp32 mainly.
    """

    def __init__(self, 
                 config: dict):

        print('-'*60)
        print("Starting actuators controller...")

        self.config = config["sub_topics"]

        # sets the pins specified in the config as output
        print("Setting pins as output...")
        self.set_pins()
        print("ActuatorsController initialized!")

    def set_pins(self):

        """
            This function sets the pins as output.
        """

        # for each variable in the config file 
        # and for each command on the variable ("up" or "down")
        # it sets a Pin object to perform the action

        for variable_alias in self.config.keys():

            for command in self.config[variable_alias]["exec"].keys():

                pin_num = self.config[variable_alias]["exec"][command]['pin_number']
                self.config[variable_alias]["exec"][command]["pin"] = Pin( pin_num,
                                                                           mode  = Pin.OUT)

                self.config[variable_alias]["exec"][command]["pin"].value(0)


    def isNumber(field: str) -> bool:

        """
            Checks if a string is a number.

            Keep in mind that the field for the codes to execute actions
            on pins, is at the same level of other fields that are strings.
            So in order to be send correctly orders to the pins, this 
            check should be done.
        """

        for i in range(len(field)):

            if field[i].isdigit() != True:
                return False
 
        return True

    def command_to_variable(self,
                            variable_alias: str,
                            command:        str):


        """
            This function turns on or off an actuator.

            INPUT: 
                    command: "1", "-1" or "0".

                             "1" means increase value of variable, 
                             "-1" means decrease value of variable,
                             "0" means leave it as it is.

                    variable_alias: alias asigned to the ambiental variable to be controlled.
        """


        if variable_alias not in self.config.keys():
            return
        
        # if the command is not in the list of commands for the variable for execution, and it's not
        # the "0" command, it returns. Because the "0" command is used to turn off 
        # all of the actuators of the variable.
        if (command not in self.config[variable_alias]["exec"].keys()) and (command != "0"):
            return


        if command == "0":

            # turns off every other command except the one specified
            for code in self.config[variable_alias]["exec"].keys():

                self.config[variable_alias]["exec"][code]["pin"].value(0)
                print("turn off {0}, {1}".format(variable_alias, code))

        if command != "0":

            for code in self.config[variable_alias]["exec"].keys():

                if code == command:
                    self.config[variable_alias]["exec"][code]["pin"].value(1)
                    print("turn on {0}, {1}".format(variable_alias, code))

                else:
                    self.config[variable_alias]["exec"][code]["pin"].value(0)
                    print("turn off {0}, {1}".format(variable_alias, code))

        print("-"*60)

    def test_actuators(self, wait_time = 4):

        # turns on every actuator

        for variable_alias in self.config.keys():
            for command in self.config[variable_alias]["exec"].keys():

                self.command_to_variable(variable_alias, command)
                sleep(wait_time)

            self.command_to_variable(variable_alias, "0")














