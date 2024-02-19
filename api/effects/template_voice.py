# effects/template_voice.py
import numpy as np
import pyaudio
import threading

class BaseVoiceEffect:
    def __init__(self, rate=44100, channels=1, chunk_size=1024):
        self.rate = rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream_in = None
        self.stream_out = None
        self.running = False
        self.thread = None  # Thread pour le traitement audio

    def process_audio(self, data):
        raise NotImplementedError("????")

    def start(self):
        if self.running:
            return  # L'effet est déjà en cours, donc on ne fait rien.
        self.running = True
        self.stream_in = self.audio.open(format=pyaudio.paInt16, channels=self.channels,
                                         rate=self.rate, input=True,
                                         frames_per_buffer=self.chunk_size)
        self.stream_out = self.audio.open(format=pyaudio.paInt16, channels=self.channels,
                                          rate=self.rate, output=True,
                                          frames_per_buffer=self.chunk_size)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while self.running:
            data = self.stream_in.read(self.chunk_size, exception_on_overflow=False)
            processed_data = self.process_audio(data)
            self.stream_out.write(processed_data)

    def stop(self):
        if not self.running:
            return  # L'effet n'est pas en cours, donc on ne fait rien.
        self.running = False
        if self.thread:
            self.thread.join()  # Attendre que le thread de traitement se termine proprement
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out.stop_stream()
        self.stream_out.close()
        self.audio.terminate()
        self.thread = None
