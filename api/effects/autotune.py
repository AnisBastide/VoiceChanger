#!/usr/bin/python3
import argparse
import numpy as np
import librosa

from effects.template_voice import BaseVoiceEffect

SEMITONES_IN_OCTAVE = 12

class AutoTuneVoiceEffect(BaseVoiceEffect):
    def __init__(self):
        super().__init__()
        self.scale = "major"  # Choisir l'échelle musicale
        self.correction_method = "closest"
        self.fmin = librosa.note_to_hz('C2')
        self.fmax = librosa.note_to_hz('C7')
        self.frame_length = 2048
        self.hop_length = self.frame_length // 4

    def degrees_from(self, scale):
        degrees = librosa.key_to_degrees(scale)
        degrees = np.concatenate((degrees, [degrees[0] + SEMITONES_IN_OCTAVE]))
        return degrees

    def closest_pitch(self, f0):
        midi_note = np.around(librosa.hz_to_midi(f0))
        nan_indices = np.isnan(f0)
        midi_note[nan_indices] = np.nan
        return librosa.midi_to_hz(midi_note)

    def closest_pitch_from_scale(self, f0):
        if np.isnan(f0):
            return np.nan
        degrees = self.degrees_from(self.scale)
        midi_note = librosa.hz_to_midi(f0)
        degree = midi_note % SEMITONES_IN_OCTAVE
        degree_id = np.argmin(np.abs(degrees - degree))
        degree_difference = degree - degrees[degree_id]
        midi_note -= degree_difference
        return librosa.midi_to_hz(midi_note)

    def autotune(self, audio):
        f0, _ = librosa.piptrack(y=audio, sr=44100, fmin=self.fmin, fmax=self.fmax)
        corrected_f0 = np.apply_along_axis(self.closest_pitch_from_scale, 0, f0)
        return corrected_f0

    def process_audio(self, data):
        corrected_f0 = self.autotune(data)

        # Conversion des fréquences de pitch en demi-tons
        semitones = librosa.hz_to_midi(corrected_f0) - librosa.note_to_midi('C2')

        # Appliquer le pitch-shift sur les données audio
        shifted_data = librosa.effects.pitch_shift(data, 44100, n_steps=semitones)

        # Lecture du flux audio pitch-shifté
        # sd.play(shifted_data, samplerate=44100)
        return shifted_data.tobytes()

    def start(self):
        super().start()
        print("Effet Auto-tune démarré. Prêt à moduler le son.")

    def stop(self):
        super().stop()
        print("Effet Auto-tune arrêté.")