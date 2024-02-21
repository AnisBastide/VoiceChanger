import numpy as np
from effects.template_voice import BaseVoiceEffect
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class OctaveurVoiceEffect(BaseVoiceEffect):

    def __init__(self, rate=44100, channels=1, chunk_size=1024):
        super().__init__(rate, channels, chunk_size)
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.channel = AnalogIn(ads, ADS.P0)
        self.factor = 0.5

    def process_audio(self, data):
        # Convertir les données audio en tableau numpy
        audio_data = np.frombuffer(data, dtype=np.int16)
        if self.channel.voltage > 0.2:
            self.factor = 0.5 + (self.channel.voltage - 0) * (1.5 - 0.5) / (3.3 - 0)
        # Appliquer l'effet d'octaveur
        audio_data_octave = self.octaveur(audio_data, self.factor)

        # Convertir les données audio octavées en bytes
        processed_data = audio_data_octave.astype(np.int16).tobytes()
        return processed_data

    def octaveur(self, signal, facteur_octave):
        # Appliquer une interpolation temporelle pour changer la vitesse de lecture
        signal_octave = np.interp(np.arange(0, len(signal), facteur_octave), np.arange(len(signal)), signal)
        return signal_octave

    def start(self):
        super().start()
        print("Effet Octaveur démarré. Prêt à moduler le son.")

    def stop(self):
        super().stop()
        print("Effet Octaveur arrêté.")