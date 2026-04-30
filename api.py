"""API 层（FastAPI 路由、会话管理）"""

from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi import Query

from game import GameEngine
from player import Player
from item import TradeableItem
from room import Room
from npc import NPC

# 初始化 FastAPI
app = FastAPI(title="文字冒险游戏 API", version="1.0")

# 游戏引擎实例（单例）
game_engine = GameEngine()

# Pydantic 模型
class TradeRequest(BaseModel):
    player_id: str
    item_name: str
    npc_name: str
    quantity: int = 1

class TradeResponse(BaseModel):
    success: bool
    message: str
    item: Optional[Dict[str, Any]] = None
    quantity: Optional[int] = None
    remaining_gold: Optional[int] = None

class PlayerState(BaseModel):
    health: int
    max_health: int
    attack: int
    gold: int
    inventory_size: int
    max_inventory_size: int
    current_room: str

# 依赖项：获取游戏引擎
def get_game_engine() -> GameEngine:
    return game_engine

# 依赖项：获取玩家
def get_player(player_id: str, engine: GameEngine = Depends(get_game_engine)) -> Player:
    player = engine.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="玩家不存在")
    return player

# 端点定义
@app.post("/actions/trade", response_model=TradeResponse)
async def trade_item(
    request: TradeRequest,
    engine: GameEngine = Depends(get_game_engine)
):
    """
    玩家与 NPC/商店交易物品
    
    - **player_id**: 玩家 ID
    - **item_name**: 要购买的物品名称
    - **npc_name**: NPC/商店名称
    - **quantity**: 购买数量（默认 1）
    """
    # 获取玩家
    player = engine.get_player(request.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="玩家不存在")
    
    # 获取 NPC
    npc = None
    for room_npc in player.current_room.npcs:
        if room_npc.name.lower() == request.npc_name.lower():
            npc = room_npc
            break
    
    if not npc:
        raise HTTPException(status_code=404, detail="NPC 不存在")
    
    # 获取物品
    item = None
    for inv_item in npc.inventory:
        if inv_item.name.lower() == request.item_name.lower() and isinstance(inv_item, TradeableItem):
            item = inv_item
            break
    
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    # 执行交易
    result = engine.trade_item(player, item, npc, request.quantity)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    # 构建响应
    return TradeResponse(
        success=result["success"],
        message=result["message"],
        item={
            "name": result["item"].name,
            "description": result["item"].description,
            "price": result["item"].price
        } if result.get("item") else None,
        quantity=result.get("quantity"),
        remaining_gold=result.get("remaining_gold")
    )

@app.get("/player/{player_id}", response_model=PlayerState)
async def get_player_state(
    player: Player = Depends(get_player)
):
    """获取玩家状态"""
    return PlayerState(
        health=player.health,
        max_health=player.max_health,
        attack=player.attack,
        gold=player.gold,
        inventory_size=len(player.inventory),
        max_inventory_size=player.max_inventory_size,
        current_room=player.current_room.name
    )

@app.post("/player/{player_id}/create")
async def create_player(
    player_id: str,
    engine: GameEngine = Depends(get_game_engine)
):
    """创建新玩家"""
    if engine.get_player(player_id):
        raise HTTPException(status_code=400, detail="玩家已存在")
    
    # 创建初始房间
    starting_room = Room("起始房间", "你站在一片神秘的森林中。")
    engine.create_player(player_id, starting_room)
    
    return {"message": f"玩家 {player_id} 创建成功"}

@app.post("/player/{player_id}/move")
async def move_player(
    player_id: str,
    direction: str = Query(..., description="移动方向 (north, south, east, west)"),
    engine: GameEngine = Depends(get_game_engine)
):
    """移动玩家"""
    player = engine.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="玩家不存在")
    
    success = player.move(direction.lower())
    if not success:
        raise HTTPException(status_code=400, detail="无法向该方向移动")
    
    return {
        "success": True,
        "message": f"已移动到 {player.current_room.name}",
        "current_room": player.current_room.name
    }