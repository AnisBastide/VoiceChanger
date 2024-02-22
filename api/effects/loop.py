import numpy as np
import pyaudio
import threading
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Set Button and LED pins
Button = 21
#Setup Button and LED
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)


class LoopVoiceEffect:
    def __init__(self, rate=44100, channels=1, chunk_size=1024):
        self.rate = rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream_in = None
        self.stream_out = None
        self.running = False
        self.thread = None
        self.is_recording = False
        self.loop_buffer = np.array([], dtype=np.int16)
        self.current_playback_position = 0  # Initialisez la position de lecture ici

    def process_audio(self):
        while self.running:
            data = self.stream_in.read(self.chunk_size, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Ajouter ici pour entendre en temps réel plus la boucle
            if not self.is_recording and self.loop_buffer.size > 0:
                # Calcul pour la lecture en boucle
                start_index = self.current_playback_position * self.chunk_size
                end_index = start_index + self.chunk_size
                if end_index > self.loop_buffer.size:
                    # Si on dépasse la taille, on combine la fin et le début pour une boucle fluide
                    looped_audio = np.concatenate(
                        (self.loop_buffer[start_index:], self.loop_buffer[:end_index % self.loop_buffer.size]))
                    self.current_playback_position = (end_index % self.loop_buffer.size) // self.chunk_size
                else:
                    looped_audio = self.loop_buffer[start_index:end_index]
                    self.current_playback_position += 1
                self.stream_out.write(looped_audio.tobytes())
            elif self.is_recording:
                self.loop_buffer = np.append(self.loop_buffer, audio_data)
                # Écrire également l'audio en direct pour entendre ce qui est enregistré
                self.stream_out.write(data)
            else:
                # Si aucun enregistrement ou boucle, jouer directement l'audio entrant
                self.stream_out.write(data)

    def toggle_recording(self,channel):
        self.is_recording = not self.is_recording
        if not self.is_recording:
            print("Enregistrement terminé, prêt à jouer en boucle.")
        else:
            self.loop_buffer = np.array([], dtype=np.int16)
            print("Enregistrement commencé. Appuyez à nouveau sur CTRL pour arrêter.")

    def start(self):
        self.running = True
        self.stream_in = self.audio.open(format=pyaudio.paInt16, channels=self.channels,
                                         rate=self.rate, input=True,
                                         frames_per_buffer=self.chunk_size)
        self.stream_out = self.audio.open(format=pyaudio.paInt16, channels=self.channels,
                                          rate=self.rate, output=True,
                                          frames_per_buffer=self.chunk_size)
        self.thread = threading.Thread(target=self.process_audio)
        self.thread.start()

        #self.is_recording = True
        # threading.Timer(5, self.toggle_recording).start()
        GPIO.add_event_detect(Button, GPIO.RISING, callback=self.toggle_recording, bouncetime=300)
        print("Effet Loop démarré. Appuyez sur CTRL pour commencer/arrêter l'enregistrement.")



    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out.stop_stream()
        self.stream_out.close()
        self.audio.terminate()
        GPIO.remove_event_detect(Button)
        print("Effet Loop arrêté.")