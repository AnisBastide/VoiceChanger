import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
pin_potentiometer = 17  # Remplacez ceci par le numéro de broche de votre potentiomètre

# Configuration de la bibliothèque RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_potentiometer, GPIO.IN)

# Configuration du fichier journal
log_file_path = "potentiometer_log.txt"

# Fonction pour lire la valeur du potentiomètre
def read_potentiometer_value():
    return GPIO.input(pin_potentiometer)

# Fonction pour enregistrer la valeur dans le fichier journal
def log_value(value):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {value}\n")

# Boucle principale
try:
    while True:
        pot_value = read_potentiometer_value()
        log_value(pot_value)
        time.sleep(1)  # Vous pouvez ajuster la fréquence de lecture ici

except KeyboardInterrupt:
    print("Arrêt du programme par l'utilisateur.")

finally:
    GPIO.cleanup()
