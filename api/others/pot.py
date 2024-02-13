# This Raspberry Pi code was developed by newbiely.com
# This Raspberry Pi code is made available for public use without any restriction
# For comprehensive instructions and wiring diagrams, please visit:
# https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-potentiometer


import time
import Adafruit_ADS1x15

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1

# Main loop to read and display the analog value
try:
    while True:
        # Read the raw analog value from channel A3
        raw_value = adc.read_adc(3, gain=GAIN)

        # Convert the raw value to voltage
        voltage = raw_value / 32767.0 * 4.096  # Assumes 4.096 V range for GAIN=1

        # Print the results
        print("Raw Value: {} \t Voltage: {:.2f} V".format(raw_value, voltage))

        # Add a delay between readings (adjust as needed)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting the program.")
