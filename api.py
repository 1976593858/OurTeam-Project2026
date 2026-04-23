from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pydantic import validator
import uuid

from game import Game

app = FastAPI(
    title="文字冒险游戏 API",
    description="OurTeam-Project2026",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

sessions: dict[str, Game] = {}


class NewGameResponse(BaseModel):
    session_id: str
    current_room: str
    description: str
    exits: List[str]
    inventory: List[str]
    message: str


class ActionRequest(BaseModel):
    session_id: str
    command: str

    @validator('command')
    def validate_command(cls, v):
        if not v or not v.strip():
            raise ValueError('命令不能为空')
        return v.strip()


class ActionResponse(BaseModel):
    session_id: str
    current_room: str
    description: str
    exits: List[str]
    inventory: List[str]
    message: str


def build_state(session_id: str, game: Game, message: str = "") -> dict:
    room = game.player.current_room
    return {
        "session_id": session_id,
        "current_room": room.name,
        "description": room.description,
        "exits": list(room.exits.keys()),
        "inventory": [item.name for item in game.player.inventory],
        "message": message
    }


@app.post("/api/v1/game/new", response_model=NewGameResponse, tags=["Game"])
def new_game():
    session_id = str(uuid.uuid4())[:8]
    game = Game()
    sessions[session_id] = game
    return build_state(session_id, game, message="游戏开始！输入 look 查看周围环境。")


@app.post("/api/v1/game/action", response_model=ActionResponse, tags=["Game"])
def do_action(req: ActionRequest):
    game = sessions.get(req.session_id)
    if not game:
        raise HTTPException(status_code=404, detail="会话不存在或已过期，请重新创建游戏")

    message = game._process_command(req.command)
    return build_state(req.session_id, game, message=message)


@app.get("/api/v1/game/{session_id}/state", response_model=ActionResponse, tags=["Game"])
def get_state(session_id: str):
    game = sessions.get(session_id)
    if not game:
        raise HTTPException(status_code=404, detail="会话不存在")
    return build_state(session_id, game)


@app.delete("/api/v1/game/{session_id}", tags=["Game"])
def end_game(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")
    del sessions[session_id]
    return {"message": "游戏会话已结束", "session_id": session_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
