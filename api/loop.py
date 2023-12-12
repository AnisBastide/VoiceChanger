import pyaudio
import wave
import threading
import vlc
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
Button = 21
GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Paramètres d'enregistrement
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

WAVE_OUTPUT_FILENAME = "enregistrement.wav"

audio = pyaudio.PyAudio()
player = vlc.MediaPlayer()

recording = False
loop_audio = False


def record_audio():
    global recording
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

    player.set_media(vlc.Media(WAVE_OUTPUT_FILENAME))
    player.play()


def play_audio():
    global loop_audio
    global recording
    while True:

        button_state = GPIO.input(Button)
        if button_state == 0 and not recording:
            loop_audio = False
            threading.Thread(target=record_audio).start()
            recording = True
        elif button_state == 0 and recording:
            recording = False
        elif not recording:
            if not loop_audio:
                if not player.get_state() == vlc.State.Playing:
                    player.set_media(vlc.Media(WAVE_OUTPUT_FILENAME))
                player.play()
                loop_audio = True
            else:
                player.stop()
                loop_audio = False


audio.terminate()
play_audio()
