from machine import Pin, ADC
from time import sleep


class Ph():

    def __init__(self, 
                 pin_number: int):
        
        self.ph_sensor = ADC(Pin(pin_number))
        self.ph_sensor.atten(ADC.ATTN_11DB)         #Full range: 3.3v
        self.ph_sensor.width(ADC.WIDTH_12BIT)       #12-bit resolution, range 0 to 4095 


    def read_ph(self,
                nsamples  = 5,
                max_iters = 10,
                rest_time = 1) -> float:

        """
            Read the pH sensor and return the average value.

            INPUTS: nsamples: number of samples to take
                    max_iters: maximum number of iterations to reach 
                               the desired number of samples
                    rest_time: time to wait between samples
        
            OUTPUT: pH value
        """

        # stores nsamples measurements from the ph sensor
        ph_samples = []
        tries = 0

        # read data until gets nsamples that are valid or
        # max_iters is reached

        while (len(ph_samples) < nsamples) and (tries < max_iters):

            voltage  = self.ph_sensor.read() * (3.3/4095.0)
            ph_value = 3.3 * voltage
            
            if (ph_value > 0) and (ph_value < 14):
                ph_samples.append(ph_value)
                
            # waits for rest_time seconds and then increases
            # tries counter
            sleep(rest_time)
            tries += 1

        # calculate average of the nsamples measurements
        ph_value = sum(ph_samples) / len(ph_samples)

        return ph_value


