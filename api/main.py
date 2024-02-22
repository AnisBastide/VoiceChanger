import os
from datetime import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import sqlite3


from effects.demon import DemonVoiceEffect
from effects.echo import EchoVoiceEffect
from effects.robot import RobotVoiceEffect
from effects.loop import LoopVoiceEffect
from effects.wahwah import WahWahEffect
from effects.octaveur import OctaveurVoiceEffect
from effects.distortion import DistortionEffect
from effects.overdrive import OverdriveVoiceEffect

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

app = FastAPI()
# Configurer CORS pour permettre toutes les origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuster ceci en fonction de vos besoins de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_effect = None
#connection = sqlite3.connect("database.db")
#cursor = connection.cursor()
#cursor.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER, name TEXT, age INTEGER)")

@app.get("/echo/{echo_value}")
async def echo(echo_value: float):
    global current_effect
    try:
        current_effect.updateValue(echo_value)
    except Exception as e:
        return {"error": str(e)}

@app.get("/start/{effect_name}")
async def start_effect(effect_name: str):
    global current_effect
    if current_effect:
        current_effect.stop()
        current_effect = None

    if effect_name == "demon":
        current_effect = DemonVoiceEffect()
    elif effect_name == "robot":
        current_effect = RobotVoiceEffect()
    elif effect_name == "echo":
        current_effect = EchoVoiceEffect()
    elif effect_name == "loop":
        current_effect = LoopVoiceEffect()
    elif effect_name == "overdrive":
        current_effect = OverdriveVoiceEffect()
    elif effect_name == "octaveur":
        current_effect = OctaveurVoiceEffect()
    elif effect_name == "wahwah":
        current_effect = WahWahEffect()
    elif effect_name == "distortion":
        current_effect = DistortionEffect()
    else:
        return {"error": "Effet inconnu"}
    current_effect.start()
    return {"status": f"Effet {effect_name} démarré"}


@app.get("/stop")
async def stop_effect():
    global current_effect
    if current_effect:
        current_effect.stop()
        current_effect = None
        return {"status": "Effet arrêté"}
    else:
        return {"error": "Aucun effet en cours de fonctionnement"}


@app.get("/effects")
async def effects():
    effects_list = []
    files = os.listdir("effects")
    for file in files:
        file_name = file.removesuffix(".py")
        if not file_name.startswith("__") and not file_name.startswith("template"):
            effects_list.append(file_name)
    return effects_list

@app.get("/record")
async def record():
    global current_effect
    if current_effect:
        GPIO.output(21, GPIO.HIGH)
        time.sleep(0.1)  # You may need to adjust this delay based on your requirements
        GPIO.output(21, GPIO.LOW)
    return 'success'



def start_loop(channel):
    global current_effect
    current_effect = LoopVoiceEffect()
    current_effect.start()
    print('Effet Loop Démarré')


GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(20, GPIO.RISING, callback=start_loop, bouncetime=300)

def start_wahwah(channel):
    global current_effect
    current_effect = WahWahEffect()
    current_effect.start()
    print('Effet WahWah Démarré')


GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(19, GPIO.RISING, callback=start_wahwah, bouncetime=300)


def start_echo(channel):
    global current_effect
    current_effect = EchoVoiceEffect()
    current_effect.start()
    print('Effet Echo Démarré')


GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(16, GPIO.RISING, callback=start_echo, bouncetime=300)


def start_overdrive(channel):
    global current_effect
    current_effect = OverdriveVoiceEffect()
    current_effect.start()
    print('Effet Overdrive Démarré')


GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(26, GPIO.RISING, callback=start_overdrive, bouncetime=300)


def stop_effect_button(channel):
    global current_effect
    if current_effect:
        current_effect.stop()
        current_effect = None
        print('Effet arrêté')


GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(13, GPIO.RISING, callback=stop_effect_button, bouncetime=300)

