import numpy as np
from effects.template_voice import BaseVoiceEffect

class OctaveurVoiceEffect(BaseVoiceEffect):
    def process_audio(self, data):
        # Convertir les données audio en tableau numpy
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Appliquer l'effet d'octaveur
        audio_data_octave = self.octaveur(audio_data, 0.5)

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