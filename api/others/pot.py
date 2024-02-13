import time
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115

# Création de l'objet I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Création de l'objet ADC en utilisant l'interface I2C
ads = ADS1115(i2c)

# Configuration du gain
ads.gain = 1

# Création d'un objet analogique pour lire depuis le canal A3
chan = AnalogIn(ads, ADS1115.P3)

# Boucle principale pour lire et afficher la valeur analogique
try:
    while True:
        # Lire la valeur et la tension
        print("Raw Value: {} \t Voltage: {:.2f} V".format(chan.value, chan.voltage))

        # Délai entre les lectures
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting the program.")