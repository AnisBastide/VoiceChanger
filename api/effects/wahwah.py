import numpy as np
from scipy.signal import butter, lfilter

from effects.template_voice import BaseVoiceEffect

class WahWahEffect(BaseVoiceEffect):
    def __init__(self, rate):
        super().__init__(rate)
        self.carrier_frequency = 30
        self.modulation_range = 400
        self.q_factor = 2.0
        self.center_frequency = 800.0

    def process_audio(self, data):
        audio_data = np.frombuffer(data, dtype=np.int16)

        t = np.arange(len(audio_data)) / self.rate
        carrier = np.sin(2 * np.pi * self.carrier_frequency * t)

        self.center_frequency = self.center_frequency + self.modulation_range * carrier
        self.center_frequency = np.clip(self.center_frequency, 400, 1200)

        b, a = butter(2, [self.center_frequency - self.q_factor/2,
                          self.center_frequency + self.q_factor/2], btype='band')

        filtered_audio = lfilter(b, a, audio_data)

        normalized_audio = np.int16(filtered_audio / np.max(np.abs(filtered_audio)) * 32767)

        processed_data = normalized_audio.tobytes()
        return processed_data

    def start(self):
        super().start()
        print("Effet Wah Wah démarré.")

    def stop(self):
        super().stop()
        print("Effet Wah Wah arrêté.")