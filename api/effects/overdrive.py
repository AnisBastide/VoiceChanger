import numpy as np
from effects.template_voice import BaseVoiceEffect

class OverdriveVoiceEffect(BaseVoiceEffect):
    def process_audio(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_data = audio_data / 32768.0
        distorted_signal = self.overdrive(audio_data, 2, 0.5)
        processed_data = (distorted_signal * 32767.0).astype(np.int16).tobytes()
        return processed_data

    def overdrive(self, signal, gain, threshold):
        distortion = np.where(signal > threshold, 1, signal / threshold)
        distorted_signal = distortion * gain * signal
        return np.clip(distorted_signal, -1, 1)

    def start(self):
        super().start()
        print("Effet Overdrive démarré. Prêt à moduler le son.")

    def stop(self):
        super().stop()
        print("Effet Overdrive arrêté.")