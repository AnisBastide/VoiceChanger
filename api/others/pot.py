import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class pot():
    def start(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        channel = AnalogIn(ads, ADS.P0)

        # Loop to read the analog input continuously
        while True:
            print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)