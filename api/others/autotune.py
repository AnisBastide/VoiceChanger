import numpy as np
import pyaudio
import threading
import librosa

from effects.template_voice import BaseVoiceEffect

class AutoTuneVoiceEffect(BaseVoiceEffect):
    def __init__(self, scale="C:major", rate=44100, channels=1, chunk_size=1024, n_fft=512):
        super().__init__(rate=rate, channels=channels, chunk_size=chunk_size)
        self.scale = scale
        self.n_fft = n_fft
        self.fmin = librosa.note_to_hz('C2')
        self.fmax = librosa.note_to_hz('C7')

    def degrees_from(self, scale):
        degrees = librosa.key_to_degrees(scale)
        degrees = np.concatenate((degrees, [degrees[0] + 12]))
        return degrees

    def closest_pitch(self, f0):
        midi_note = np.around(librosa.hz_to_midi(f0))
        nan_indices = np.isnan(f0)
        midi_note[nan_indices] = np.nan
        return librosa.midi_to_hz(midi_note)

    def closest_pitch_from_scale(self, f0):
        if np.any(np.isnan(f0)):
            return np.nan
        degrees = self.degrees_from(self.scale)
        midi_note = librosa.hz_to_midi(f0)
        degree = midi_note % 12
        degree = np.repeat(degree, len(degrees))
        degree_id = np.argmin(np.abs(degrees - degree))
        degree_difference = degree - degrees[degree_id]
        midi_note -= degree_difference
        return librosa.midi_to_hz(midi_note)

    def autotune(self, audio):
        f0, _ = librosa.piptrack(y=audio, sr=self.rate, fmin=self.fmin, fmax=self.fmax, n_fft=self.n_fft)
        corrected_f0 = np.apply_along_axis(self.closest_pitch_from_scale, 0, f0)
        return corrected_f0

    def process_audio(self, data):
        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        corrected_f0 = self.autotune(audio)
        processed_data = corrected_f0.astype(np.int16).tobytes()
        return processed_data

    def start(self):
        super().start()
        print("Effet autotune démarré. Prêt à moduler le son.")

    def stop(self):
        super().stop()
        print("Effet autotune arrêté.")
