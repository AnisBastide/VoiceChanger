import numpy as np
from effects.template_voice import BaseVoiceEffect

class ReverbVoiceEffect(BaseVoiceEffect):
    def process_audio(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)
        echoed_samples = audio_data + self.prev_samples * self.decay
        self.prev_samples = np.roll(echoed_samples, self.delay_samples)

        return echoed_samples.astype(np.int16).tobytes()

    def start(self):
        super().start()
        print("Effet Réverbération démarré.")

    def stop(self):
        super().stop()
        print("Effet Réverbération arrêté.")
