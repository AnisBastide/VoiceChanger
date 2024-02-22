import numpy as np
from effects.template_voice import BaseVoiceEffect

class DistortionEffect(BaseVoiceEffect):
    def __init__(self, rate):
        super().__init__(rate)
        self.gain = 2.0

    def process_audio(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)
        distorted_audio = np.clip(audio_data * self.gain, -32768, 32767)
        processed_data = distorted_audio.astype(np.int16).tobytes()
        return processed_data

    def start(self):
        super().start()
        print("Effet de distorsion démarré.")

    def stop(self):
        super().stop()
        print("Effet de distorsion arrêté.")