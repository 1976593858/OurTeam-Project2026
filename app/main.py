from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.game_engine import GameEngine

app = FastAPI(title="MUD Web API")
engine = GameEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/state")
def get_state():
    return engine.get_state()

@app.post("/api/move")
def move(data: dict):
    return engine.move(data["dir"])