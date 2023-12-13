import pyaudio
import numpy as np
from scipy.signal import hilbert

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()
def process_audio(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    carrier = np.sin(2 * np.pi * 30 * np.arange(len(audio_data)) / RATE)
    modulated = np.real(hilbert(audio_data) * carrier)
    processed_data = modulated.astype(np.int16).tobytes()
    return processed_data


stream_in = audio.open(format=FORMAT, channels=CHANNELS,
                       rate=RATE, input=True,
                       frames_per_buffer=CHUNK)
stream_out = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True,
                        frames_per_buffer=CHUNK)

print("Enregistrement en cours...")


try:
    while True:
        data = stream_in.read(CHUNK)
        processed_data = process_audio(data)
        stream_out.write(processed_data)
except KeyboardInterrupt:
    print("Arrêt de l'enregistrement...")

stream_in.stop_stream()
stream_in.close()
stream_out.stop_stream()
stream_out.close()
audio.terminate()