import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
pin_potentiometer = 17  # Remplacez ceci par le numéro de broche de votre potentiomètre

# Configuration de la bibliothèque RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_potentiometer, GPIO.IN)

# Fonction pour lire la valeur du potentiomètre (0-1023 pour un potentiomètre 10 bits)
def read_potentiometer_value():
    return GPIO.input(pin_potentiometer)  # Pour un potentiomètre 10 bits

# Boucle principale
try:
    while True:
        pot_value = read_potentiometer_value()
        print(f"Valeur du potentiomètre : {pot_value}")
        time.sleep(1)  # Vous pouvez ajuster la fréquence de lecture ici

except KeyboardInterrupt:
    print("Arrêt du programme par l'utilisateur.")

finally:
    GPIO.cleanup()
