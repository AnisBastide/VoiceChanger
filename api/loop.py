import pyaudio
import wave
import threading
import os
from pynput import keyboard
import pygame

# Paramètres d'enregistrement
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

WAVE_OUTPUT_FILENAME = "recordedFile.wav"

audio = pyaudio.PyAudio()
pygame.mixer.init()
recording = False
loop_audio = False

def record_audio():
    global recording
    recording = True
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Enregistrement en cours...")
    frames = []

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("Fin de l'enregistrement...")

    stream.stop_stream()
    stream.close()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    pygame.mixer.music.load(WAVE_OUTPUT_FILENAME)
    if loop_audio:
        pygame.mixer.music.play(-1)
def play_audio():
    global loop_audio
    if not loop_audio:
        if pygame.mixer.music.get_busy() == 0:
            pygame.mixer.music.load(WAVE_OUTPUT_FILENAME)
        pygame.mixer.music.play(loops=-1)
        loop_audio = True
    else:
        pygame.mixer.music.stop()
        loop_audio = False

def on_press(key):
    global recording, loop_audio
    if key == keyboard.Key.ctrl_l and not recording:
        threading.Thread(target=record_audio).start()
        recording = True
    if key == keyboard.Key.alt_l and recording:
        recording = False
    if key == keyboard.Key.ctrl_r:
        play_audio()

with keyboard.Listener(on_release=on_press) as listener:
    listener.join()

audio.terminate()