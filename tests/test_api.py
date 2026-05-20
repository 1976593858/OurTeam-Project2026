"""API 层单元测试"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


class TestAPI:
    """API 端点测试"""

    def test_create_player(self):
        """测试创建玩家端点"""
        response = client.post("/player/test_user_123/create")
        assert response.status_code == 200
        assert "创建成功" in response.json()["message"]

    def test_create_existing_player(self):
        """测试创建已存在的玩家"""
        client.post("/player/test_user_456/create")
        response = client.post("/player/test_user_456/create")
        assert response.status_code == 400

    def test_get_player_state(self):
        """测试获取玩家状态"""
        client.post("/player/test_user_789/create")
        response = client.get("/player/test_user_789")
        assert response.status_code == 200
        data = response.json()
        assert "health" in data
        assert "gold" in data

    def test_move_player(self):
        """测试移动玩家"""
        client.post("/player/test_user_move/create")
        response = client.post("/player/test_user_move/move?direction=north")
        assert response.status_code == 400  # 初始房间没有 north 出口
