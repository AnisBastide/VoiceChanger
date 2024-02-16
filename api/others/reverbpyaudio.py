import pyaudio
import numpy as np

def add_echo(signal, delay_factor=1, decay=0.9):
    # Créer une enveloppe de réverbération exponentielle
    envelope = decay ** np.arange(int(delay_factor * len(signal)))

    # Normaliser l'enveloppe pour éviter une amplification excessive
    envelope /= np.max(envelope)

    # Appliquer l'écho en convoluant le signal avec l'enveloppe
    echoed_signal = np.convolve(signal, envelope, mode='full')[:len(signal)]

    return echoed_signal

def audio_callback(in_data, frame_count, time_info, status):
    if status:
        print(status)

    # Convertir les données d'entrée en tableau numpy
    indata = np.frombuffer(in_data, dtype=np.int16)

    # Ajouter de l'écho au flux audio
    echoed_data = add_echo(indata)

    # Convertir le tableau numpy résultant en bytes
    outdata = echoed_data.astype(np.int16).tobytes()

    return outdata, pyaudio.paContinue

# Paramètres audio
sample_rate = 44100
block_size = 1024

# Initialiser l'objet PyAudio
p = pyaudio.PyAudio()

# Ouvrir le flux audio
stream = p.open(format=pyaudio.paInt16,
                channels=1,  # Utilisez 1 canal pour la simplicité
                rate=sample_rate,
                input=True,
                output=True,
                stream_callback=audio_callback,
                frames_per_buffer=block_size)

print("Reverb Effect - Enregistrement en cours...")

# Commencer la lecture en continu
stream.start_stream()

try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    # Arrêter le flux audio en cas d'interruption par l'utilisateur
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Application arrêtée.")
