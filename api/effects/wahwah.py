import numpy as np
from effects.template_voice import BaseVoiceEffect


class WahWahEffect(BaseVoiceEffect):
    def __init__(self, rate: int = 44100, depth: float = 0.5, freq_range: tuple = (400, 2000),
                 rate_range: tuple = (0.1, 2.0)):
        super().__init__(rate)
        self.depth = depth
        self.freq_range = freq_range
        self.rate_range = rate_range
        self.index = 0

    def process_audio(self, data: np.ndarray) -> np.ndarray:
        audio_data = np.frombuffer(data, dtype=np.int16)
        t = np.arange(len(audio_data)) / self.rate
        mod_range = np.linspace(self.freq_range[0], self.freq_range[1], len(audio_data))
        rate = np.interp(np.sin(2 * np.pi * self.index), [-1, 1], self.rate_range)
        self.index += rate / self.rate
        carrier = np.sin(2 * np.pi * mod_range * t)
        modulated = audio_data * (1 + self.depth * carrier)
        processed_data = modulated.astype(np.int16)
        return processed_data.tobytes()

    def start(self):
        super().start()
        print("Effet Wah-Wah démarré.")

    def stop(self):
        super().stop()
        print("Effet Wah-Wah arrêté.")
