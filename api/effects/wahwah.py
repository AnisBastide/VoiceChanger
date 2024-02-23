import numpy as np
from effects.template_voice import BaseVoiceEffect

class WahWahEffect(BaseVoiceEffect):
    def __init__(self, rate: int = 44100, depth: float = 0.5, freq_range: tuple = (400, 2000),
                 rate_range: tuple = (0.1, 2.0)):
        super().__init__(rate)
        # Profondeur de l'effet
        self.depth = depth
        # Plage de fréquences pour l'effet Wah-Wah
        self.freq_range = freq_range
        # Plage de taux de modulation
        self.rate_range = rate_range
        self.index = 0

    def process_audio(self, data: np.ndarray) -> np.ndarray:
        # Conversion des données audio en tableau numpy
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Création d'une séquence temporelle en fonction de la longueur des données audio
        t = np.arange(len(audio_data)) / self.rate
        # Création d'une séquence de fréquences modulées entre la plage spécifiée
        mod_range = np.linspace(self.freq_range[0], self.freq_range[1], len(audio_data))
        # Interpolation du taux de modulation en fonction d'une onde sinusoïdale
        rate = np.interp(np.sin(2 * np.pi * self.index), [-1, 1], self.rate_range)
        # Mise à jour de l'indice en fonction du taux de modulation
        self.index += rate / self.rate
        # Création d'une onde porteuse sinusoïdale modulée par la séquence de fréquences
        carrier = np.sin(2 * np.pi * mod_range * t)
        # Application de l'effet Wah-Wah en modulant les données audio
        modulated = audio_data * (1 + self.depth * carrier)
        # Conversion du tableau
        processed_data = modulated.astype(np.int16)
        # Conversion des données traitées
        return processed_data.tobytes()

    def start(self):
        super().start()
        print("Effet Wah-Wah démarré.")

    def stop(self):
        super().stop()
        print("Effet Wah-Wah arrêté.")
