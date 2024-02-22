import os
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from uvicorn.loops import asyncio
import sqlite3

from others.pot import pot

from effects.overdrive import OverdriveVoiceEffect
from effects.octaveur import OctaveurVoiceEffect
from effects.demon import DemonVoiceEffect
from effects.echo import EchoVoiceEffect
from effects.robot import RobotVoiceEffect
from effects.loop import LoopVoiceEffect

from effects.wahwah import WahWahEffect
from effects.distortion import DistortionEffect

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
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER, name TEXT, age INTEGER)")

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
