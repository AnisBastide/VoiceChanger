import numpy as np
import sounddevice as sd

def add_reverb(signal, decay=0.5, delay=3, sample_rate=44100):
    # Créer une enveloppe de réverbération exponentielle
    envelope = decay ** np.arange(int(delay * sample_rate))

    # Normaliser l'enveloppe pour éviter une amplification excessive
    envelope /= np.max(envelope)

    # Appliquer la réverbération en convoluant le signal avec l'enveloppe
    reverberated_signal = np.convolve(signal, envelope, mode='full')[:len(signal)]

    return reverberated_signal

def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Ajouter de la réverbération au flux audio
    reverberated_data = add_reverb(indata[:, 0])  # Utilisez le canal gauche pour la simplicité

    # Répliquer le signal pour tous les canaux
    reverberated_data = np.column_stack([reverberated_data] * indata.shape[1])

    # Envoyer le signal modifié à la sortie audio
    outdata[:] = reverberated_data

# Paramètres audio
sample_rate = 44100
block_size = 1024

# Initialiser l'objet sounddevice
sd.default.samplerate = sample_rate
sd.default.channels = 2  # Stéréo

# Configurer la réverbération
decay_factor = 0.5
delay_time = 0.5

# Ouvrir les flux d'entrée et de sortie
with sd.Stream(callback=audio_callback, blocksize=block_size):
    print("Presser Ctrl+C pour arrêter l'application.")
    sd.sleep(1000000)
