import numpy as np
from effects.template_voice import BaseVoiceEffect


class DistortionEffect(BaseVoiceEffect):
    def __init__(self, rate: int = 44100, gain: float = 0.5):
        super().__init__(rate)
        self.gain = gain

    def process_audio(self, data: np.ndarray) -> bytes:
        audio_data = np.frombuffer(data, dtype=np.int16)
        distorted_audio = np.clip(audio_data * self.gain, -32768, 32767)
        processed_data = distorted_audio.astype(np.int16)
        return processed_data.tobytes()

    def start(self):
        super().start()
        print("Effet de distorsion démarré.")

    def stop(self):
        super().stop()
        print("Effet de distorsion arrêté.")
