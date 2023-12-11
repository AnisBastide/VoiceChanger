import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create a single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Main loop
try:
    while True:
        # Read the raw ADC value
        raw_value = chan.value

        # Print the raw ADC value and voltage
        print(f"Raw Value: {raw_value}, Voltage: {chan.voltage}V")

        # Wait for a short period before reading again
        time.sleep(0.5)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    pass
finally:
    # Clean up resources
    ads.deinit()
