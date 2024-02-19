from fastapi import FastAPI
import uvicorn
from uvicorn.loops import asyncio

from effects.demon import DemonVoiceEffect
from effects.reverb import ReverbVoiceEffect
from effects.robot import RobotVoiceEffect

app = FastAPI()
current_effect = None

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
    elif effect_name == "reverb":
        current_effect = ReverbVoiceEffect()

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