import numpy as np
import pyaudio

def robot_voice_effect(signal, sample_rate=44100):
    modulator_frequency = 0.5
    carrier_frequency = 200

    t = np.arange(len(signal)) / sample_rate
    carrier = np.sin(2 * np.pi * carrier_frequency * t)

    modulated_signal = signal * carrier

    return modulated_signal.astype(np.float32)  # Convertir en format float32

def audio_callback(in_data, frame_count, time_info, status):
    if status:
        print(status)

    robot_voice = robot_voice_effect(np.frombuffer(in_data, dtype=np.float32))
    robot_voice_stereo = np.column_stack([robot_voice] * 2)
    return (robot_voice_stereo.tobytes(), pyaudio.paContinue)

sample_rate = 44100
block_size = 1024

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=block_size,
                stream_callback=audio_callback)

print("Presser Ctrl+C pour arrêter l'application.")

stream.start_stream()

try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    print("Arrêt de l'application.")

stream.stop_stream()
stream.close()
p.terminate()
