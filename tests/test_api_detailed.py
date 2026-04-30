import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api import app, game_engine
from player import Player
from room import Room


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


def test_create_player_endpoint(client):
    """测试创建玩家端点的各种情况"""
    # 测试成功创建
    response = client.post("/player/test_player/create")
    assert response.status_code == 200
    assert "message" in response.json()
    
    # 测试重复创建
    response = client.post("/player/test_player/create")
    assert response.status_code == 400
    assert "detail" in response.json()


def test_get_player_state_for_nonexistent_player(client):
    """测试获取不存在玩家的状态"""
    response = client.get("/player/nonexistent_player")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_move_player_nonexistent(client):
    """测试移动不存在的玩家"""
    response = client.post("/player/nonexistent_player/move?direction=north")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_move_player_invalid_direction(client):
    """测试移动玩家到无效方向"""
    # 先创建玩家
    client.post("/player/move_test_player/create")
    
    # 尝试移动到无效方向
    response = client.post("/player/move_test_player/move?direction=south")
    assert response.status_code == 400
    assert "detail" in response.json()


def test_trade_with_nonexistent_player(client):
    """测试与不存在的玩家交易"""
    from api import TradeRequest
    trade_request = {
        "player_id": "nonexistent_player",
        "item_name": "test_item",
        "npc_name": "test_npc",
        "quantity": 1
    }
    response = client.post("/actions/trade", json=trade_request)
    assert response.status_code == 404


def test_player_state_after_creation(client):
    """测试创建玩家后的状态"""
    # 创建玩家
    client.post("/player/state_test_player/create")
    
    # 获取玩家状态
    response = client.get("/player/state_test_player")
    assert response.status_code == 200
    
    data = response.json()
    assert "health" in data
    assert "max_health" in data
    assert "attack" in data
    assert "gold" in data
    assert "inventory_size" in data
    assert "max_inventory_size" in data
    assert "current_room" in data