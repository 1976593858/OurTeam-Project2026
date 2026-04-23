import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_create_new_game():
    response = client.post("/api/v1/game/new")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["current_room"] == "门厅"


def test_action_look():
    resp = client.post("/api/v1/game/new")
    session_id = resp.json()["session_id"]

    action = client.post(
        "/api/v1/game/action",
        json={"session_id": session_id, "command": "look"}
    )
    assert action.status_code == 200


def test_move_and_take():
    resp = client.post("/api/v1/game/new")
    session_id = resp.json()["session_id"]

    r1 = client.post(
        "/api/v1/game/action",
        json={"session_id": session_id, "command": "east"}
    )
    assert r1.json()["current_room"] == "厨房"

    r2 = client.post(
        "/api/v1/game/action",
        json={"session_id": session_id, "command": "take 苹果"}
    )
    assert "苹果" in r2.json()["inventory"]
