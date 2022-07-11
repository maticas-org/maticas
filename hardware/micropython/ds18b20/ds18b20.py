import machine, onewire, ds18x20, time


class ds18b20():

    """
    Class for managing the ds18b20 sensors/sensor.

    INPUT:
            pin_number: int

    FUNCTIONS:
            read_temperature: reads temperature of ds18b20 sensors 
                              and returns an average temperature.
    """

    def __init__(self, pin_number: int):
    
        print("-"*60)
        print("Starting ds18b20 sensor...")
        self.pin_number = pin_number
        self.ds18b20_pin = machine.Pin(self.pin_number)
        self.ds18b20_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds18b20_pin))

        # in case there are many sensors connected it 
        # can be useful to scan for them
        self.sensors_dirs = self.ds18b20_sensor.scan()
        print("Found %d sensors on bus" % len(self.sensors_dirs))

        print("Checking sensors integrity...")
        test = self.read_temperature()

        if test > 0:
            print("Sensors integrity OK!")

    def read_temperature(self,
                         nsamples = 5,
                         max_trials = 10,
                         rest_time = 0.750):
        # reads water temperature of different ds18b20 sensors
        # (it also works with only one sensor)
        # while assuring that measuremnts are valid.

        # for that purpose creates an array of nsamples of valid temperatures 
        # and averages them when giving the otput
        # in case many sensors are given, it takes an average of the averaged 
        # temperatures of all sensors

        # create array of nsamples of valid temperatures
        temp_array = []

        # create an array of averages gotten from different sensors
        temp_averages = []

        #trial counter
        trial = 0

        for sensor_dir in self.sensors_dirs:

            while (len(temp_array) <= nsamples) and (trial <= max_trials):

                try:
                    # samples temperature
                    self.ds18b20_sensor.convert_temp()
                    time.sleep(rest_time)

                    # reads temperature
                    temp = self.ds18b20_sensor.read_temp(sensor_dir)

                    # check if temperature is valid
                    if temp > 0:
                        temp_array.append(temp)

                    else:
                        print('Invalid temperature')

                except Exception as e:

                    print('Error reading temperature.')
                    print("Oops!", e.__class__, "occurred.")
                    print(e)

                    nsensors = len(self.ds18b20_sensor.scan())

                    if nsensors == 0:
                        print('No sensors found.')
                        return -1

                trial += 1
                    

            # average temperatures
            temp_average = sum(temp_array)/len(temp_array)
            temp_averages.append(temp_average)

            # reset array
            temp_array.clear()

        return sum(temp_averages)/len(temp_averages)




