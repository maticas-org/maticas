from ds18b20 import ds18b20
import time

def main():
    
    temperature_object = ds18b20(pin_number = 32)

    while True:
        # Read the temperature from the sensor
        temp = temperature_object.read_temperature()

        # Print the temperature to the screen
        print("Temperature: %s C" % temp)

        time.sleep(3)


if __name__ == "__main__":

    main()
