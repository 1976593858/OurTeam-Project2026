import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function")
def client():
    """为每个测试提供干净的测试客户端"""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def reset_game_state():
    """重置游戏状态（如果需要的话）"""
    # 这里可以添加重置游戏状态的代码
    pass