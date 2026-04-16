import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from room import Room
from item import Item


class TestRoom:
    def test_room_creation(self):
        """房间应能正确创建并保存名称和描述"""
        room = Room("入口大厅", "一个阴暗的大厅")
        assert room.name == "入口大厅"
        assert room.description == "一个阴暗的大厅"

    def test_room_starts_with_no_exits(self):
        """新建房间默认没有出口"""
        room = Room("密室", "神秘的密室")
        assert room.exits == {}

    def test_room_starts_with_no_items(self):
        """新建房间默认没有物品"""
        room = Room("空房间", "一个空房间")
        assert room.items == []

    def test_room_add_exit(self):
        """添加出口后可以通过方向找到目标房间"""
        hall = Room("大厅", "宽阔的大厅")
        garden = Room("花园", "美丽的花园")
        hall.add_exit("north", garden)
        assert hall.exits.get("north") == garden

    def test_room_add_item(self):
        """向房间添加物品后可以在物品列表中找到"""
        room = Room("储藏室", "堆满杂物的储藏室")
        key = Item("钥匙", "古老的铁钥匙")
        room.add_item(key)
        assert key in room.items