import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI()

processes = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StateModel(BaseModel):
    state: int

def start_effect(effect_name: str):
    python_executable = sys.executable
    stop_all_effects()
    processes[effect_name] = subprocess.Popen([python_executable, f"effects/{effect_name}.py"])

def stop_all_effects():
    for effect_name, process in processes.items():
        process.terminate()
        process.wait()
    processes.clear()

@app.post("/robot")
async def start_robot(data: StateModel):
    start_effect("robot")
    return {"message": "Robot effect started"}

@app.post("/demon")
async def start_demon(data: StateModel):
    start_effect("demon")
    return {"message": "Demon effect started"}

@app.post("/reverb")
async def start_reverb(data: StateModel):
    start_effect("reverbpyaudio")
    return {"message": "Reverb effect started"}

@app.post("/stop")
async def stop_effects():
    stop_all_effects()
    return {"message": "All effects stopped"}

@app.get("/")
def read_root():
    return {"Hello": "World"}
