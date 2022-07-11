from machine import Pin, ADC
from time import sleep

class Ec():

    def __init__(self,
                ec_signal_pin_number: int,
                ec_power_pin_number: int,
                ec_ground_pin_number: int,
                default_pin_resistance  = 25.0,
                default_resistance      = 1000,
                default_cell_constant   = 2.0,
                default_input_voltage   = 3.3,
                temperature_coefficient = 0.019):


        print('-'*60)
        print("Starting Ec sensor...")

        # resistance of powering pins
        self.rpin_default = default_pin_resistance

        # resistance of the sensor
        self.r_default = default_resistance

        # constant for the ec sensor
        self.k = default_cell_constant

        # temperature coefficient for the ec sensor
        self.t_coefficient = temperature_coefficient

        # input voltage for the ec sensor
        self.voltage = default_input_voltage


        self.ec_signal = ADC(Pin(ec_signal_pin_number))
        self.ec_signal.atten(ADC.ATTN_11DB)         #Full range: 3.3v
        self.ec_signal.width(ADC.WIDTH_12BIT)       #12-bit resolution, range 0 to 4095 
        
        # sets power pin and ground pin as otuputs
        self.ec_power  = Pin(ec_power_pin_number, Pin.OUT)
        self.ec_ground = Pin(ec_ground_pin_number, Pin.OUT)

        # we can leave the ground pin connected permanently
        self.ec_ground.value(0)

        print("Ec sensor ready!")

    
    def read_ec( self,
                 wtemperature: float,
                 nsamples    = 5,
                 max_iters   = 10,
                 rest_time   = 0.750 ):

        # stores nsamples measurements from the ph sensor
        ec_samples = []
        tries      = 0

        # read data until gets nsamples that are valid or
        # max_iters is reached

        while (len(ec_samples) < nsamples) and (tries < max_iters):

            # calculates the voltage drop across the sensor
            voltage_drop    = self.ec_signal.read() * (self.voltage/4095.0)
            resistance_cell = (voltage_drop * self.r_default) / (self.voltage - voltage_drop)

            # accounts for resistance of the pin
            resistance_cell = resistance_cell - self.rpin_default

            # calculates the EC 
            ec_value        = 1000/(resistance_cell * self.k)
            ec_value        = ec_value/(1 + self.t_coefficient * (wtemperature - 25))

            if  ec_value > 0:
                ec_samples.append(ec_value)
                
            # waits for rest_time seconds and then increases
            # tries counter
            sleep(rest_time)
            tries += 1

        # calculate average of the nsamples measurements
        ec_value = sum(ec_samples) / len(ec_samples)

        return ec_value


