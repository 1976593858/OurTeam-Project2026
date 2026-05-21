import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_state():
    """测试获取游戏状态接口"""
    resp = client.get("/api/state")
    assert resp.status_code == 200
    data = resp.json()
    assert "room" in data
    assert "desc" in data
    assert "exits" in data
    assert "inventory" in data
    # 验证初始房间是门厅
    assert data["room"] == "门厅"

def test_move_east():
    """测试向东移动接口"""
    resp = client.post("/api/move", json={"dir": "east"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["room"] == "厨房"
    assert "desc" in data

def test_move_west_back():
    """测试向西移动返回原房间"""
    # 先向东
    client.post("/api/move", json={"dir": "east"})
    # 再向西
    resp = client.post("/api/move", json={"dir": "west"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["room"] == "门厅"

def test_move_invalid_direction():
    """测试无效方向移动"""
    resp = client.post("/api/move", json={"dir": "invalid"})
    assert resp.status_code == 200
    data = resp.json()
    # 无效方向移动后，房间应该保持不变
    assert data["room"] == "门厅"

def test_get_state_structure():
    """测试返回数据结构完整性"""
    resp = client.get("/api/state")
    data = resp.json()
    
    # 验证所有必需字段都存在
    required_fields = ["room", "desc", "exits", "inventory"]
    for field in required_fields:
        assert field in data, f"缺少字段: {field}"
    
    # 验证数据类型
    assert isinstance(data["room"], str)
    assert isinstance(data["desc"], str)
    assert isinstance(data["exits"], list)
    assert isinstance(data["inventory"], list)

def test_multiple_moves_sequence():
    """测试连续移动序列"""
    # 向东到厨房
    resp1 = client.post("/api/move", json={"dir": "east"})
    assert resp1.json()["room"] == "厨房"
    
    # 向西回门厅
    resp2 = client.post("/api/move", json={"dir": "west"})
    assert resp2.json()["room"] == "门厅"
    
    # 再次向东到厨房
    resp3 = client.post("/api/move", json={"dir": "east"})
    assert resp3.json()["room"] == "厨房"

def test_api_response_time():
    """测试API响应时间在合理范围内"""
    import time
    start_time = time.time()
    resp = client.get("/api/state")
    end_time = time.time()
    
    assert resp.status_code == 200
    response_time = end_time - start_time
    assert response_time < 1.0, f"响应时间过长: {response_time}秒"

# def test_cors_headers():
#     """测试CORS头部是否正确设置"""
#     resp = client.options("/api/state")
#     # 检查CORS相关的响应头
#     assert resp.status_code in [200, 204]