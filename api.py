from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid

from game import Game

app = FastAPI(
    title="文字冒险游戏 API",
    description="OurTeam-Project2026 游戏接口契约，前后端联调依据",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 内存会话存储
sessions: dict[str, Game] = {}


# ---------- 数据模型 ----------

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

class ActionResponse(BaseModel):
    session_id: str
    current_room: str
    description: str
    exits: List[str]
    inventory: List[str]
    message: str


# ---------- 工具函数 ----------

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


# ---------- 接口 ----------

@app.post("/api/v1/game/new", response_model=NewGameResponse, tags=["Game"])
def new_game():
    """创建一个新的游戏会话，返回初始房间状态"""
    session_id = str(uuid.uuid4())[:8]
    game = Game()
    sessions[session_id] = game
    return build_state(session_id, game, message="游戏开始！输入 look 查看周围环境。")


@app.post("/api/v1/game/action", response_model=ActionResponse, tags=["Game"])
def do_action(req: ActionRequest):
    """
    向游戏发送一条指令。

    支持的指令示例：
    - `look` 查看房间
    - `north` / `south` / `east` / `west` 移动
    - `take 物品名` 拾取物品
    - `inventory` 查看背包
    - `quit` 结束游戏
    """
    game = sessions.get(req.session_id)
    if not game:
        raise HTTPException(status_code=404, detail="会话不存在或已过期，请重新创建游戏")

    # 捕获 _process_command 的 print 输出作为 message
    import io, sys
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        game._process_command(req.command)
    finally:
        sys.stdout = sys.__stdout__
    message = buffer.getvalue().strip()

    return build_state(req.session_id, game, message=message)


@app.get("/api/v1/game/{session_id}/state", response_model=ActionResponse, tags=["Game"])
def get_state(session_id: str):
    """查询当前游戏会话的状态（不执行任何指令）"""
    game = sessions.get(session_id)
    if not game:
        raise HTTPException(status_code=404, detail="会话不存在")
    return build_state(session_id, game)


@app.delete("/api/v1/game/{session_id}", tags=["Game"])
def end_game(session_id: str):
    """销毁指定游戏会话"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")
    del sessions[session_id]
    return {"message": "游戏会话已结束", "session_id": session_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)