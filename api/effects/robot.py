import numpy as np
from effects.template_voice import BaseVoiceEffect
class RobotVoiceEffect(BaseVoiceEffect):
    def process_audio(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)
        carrier_frequency = 440  # Fréquence en Hz
        modulator_frequency = 0.25  # Fréquence de modulation
        mod_index = 1  # Indice de modulation

        t = np.arange(len(audio_data)) / self.rate
        carrier = np.sin(2 * np.pi * carrier_frequency * t)
        modulator = np.sin(2 * np.pi * modulator_frequency * t) * mod_index

        modulated = audio_data * (1 + modulator) * carrier
        processed_data = modulated.astype(np.int16).tobytes()
        return processed_data

    def start(self):
        super().start()
        print("Effet Robot démarré. Prêt à moduler le son.")

    def stop(self):
        # Arrêt des streams et nettoyage
        super().stop()
        print("Effet Robot arrêté.")
