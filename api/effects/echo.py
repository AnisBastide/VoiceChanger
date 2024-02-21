import numpy as np
from effects.template_voice import BaseVoiceEffect

class EchoVoiceEffect(BaseVoiceEffect):
    def __init__(self, rate=44100, channels=1, chunk_size=1024, echo_delay=0.8, echo_decay=0.5):
        super().__init__(rate, channels, chunk_size)
        # Définir le délai d'écho en secondes (par exemple, 0.8 seconde)
        self.echo_delay = echo_delay
        # Définir le facteur d'atténuation de l'écho (par exemple, 0.5 pour réduire l'amplitude de 50% à chaque répétition)
        self.echo_decay = echo_decay
        # Calculer le nombre de samples correspondant au délai d'écho
        self.delay_samples = int(self.echo_delay * self.rate)
        # Initialiser un buffer circulaire pour stocker les échantillons pour l'écho
        self.echo_buffer = np.zeros(int(self.rate * self.echo_delay), dtype=np.float32)
        self.echo_buffer_index = 0

    def process_audio(self, data):
        print('test')
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        # Créer un buffer pour les données traitées
        processed_data = np.zeros_like(audio_data)

        for i in range(len(audio_data)):
            # Lire l'échantillon actuel du buffer d'écho
            echo_sample = self.echo_buffer[self.echo_buffer_index]
            # Mélanger l'échantillon d'entrée avec l'échantillon d'écho
            processed_sample = audio_data[i] + echo_sample
            # Atténuer l'échantillon d'écho et le remettre dans le buffer pour les futurs échos
            self.echo_buffer[self.echo_buffer_index] = processed_sample * self.echo_decay
            # Mettre à jour l'index du buffer circulaire
            self.echo_buffer_index = (self.echo_buffer_index + 1) % len(self.echo_buffer)
            processed_data[i] = processed_sample

        # S'assurer que les données traitées sont dans les limites valides pour int16
        processed_data = np.clip(processed_data, -32768, 32767).astype(np.int16)
        return processed_data.tobytes()

    def start(self):
        super().start()
        print("Effet d'écho démarré. Prêt à traiter.")

    def stop(self):
        super().stop()
        print("Effet d'écho arrêté.")
