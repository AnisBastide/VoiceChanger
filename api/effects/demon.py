import numpy as np
from effects.template_voice import BaseVoiceEffect

class DemonVoiceEffect(BaseVoiceEffect):
    def process_audio(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)
        carrier_frequency = 30
        t = np.arange(len(audio_data)) / self.rate
        carrier = np.sin(2 * np.pi * carrier_frequency * t)
        modulated = audio_data * carrier
        processed_data = modulated.astype(np.int16).tobytes()
        return processed_data

    def start(self):
        # Il est important de démarrer les streams d'entrée et de sortie
        super().start()
        print("Effet Démon démarré. Prêt à moduler le son.")

    def stop(self):
        super().stop()
        print("Effet Démon arrêté.")