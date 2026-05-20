import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from room import Room
from item import Item
from player import Player


class TestPlayer:
    def setup_method(self):
        """每个测试前创建一个干净的初始房间和玩家"""
        self.room = Room("测试房间", "一个用于测试的房间")
        self.player = Player(self.room)

    def test_player_starts_in_correct_room(self):
        """玩家应该从指定房间出发"""
        assert self.player.current_room == self.room

    def test_player_inventory_starts_empty(self):
        """玩家初始背包应为空"""
        assert self.player.inventory == []

    def test_player_move_to_valid_direction(self):
        """移动到有出口的方向应该成功"""
        next_room = Room("北方房间", "北边的房间")
        self.room.add_exit("north", next_room)
        result = self.player.move("north")
        assert result is True
        assert self.player.current_room == next_room

    def test_player_move_to_invalid_direction(self):
        """移动到没有出口的方向应该失败"""
        result = self.player.move("south")
        assert result is False
        assert self.player.current_room == self.room

    def test_player_take_item_success(self):
        """拾取房间内存在的可拾取物品应该成功"""
        sword = Item("剑", "一把锋利的剑")
        self.room.add_item(sword)
        result = self.player.take_item("剑")
        assert result == sword
        assert sword in self.player.inventory
        assert sword not in self.player.current_room.items

    def test_player_take_item_not_found(self):
        """拾取不存在的物品应该返回 None"""
        result = self.player.take_item("不存在的物品")
        assert result is None

    # 在现有测试基础上添加：
    def test_player_gold_operations(self):
        """测试金币操作"""
        # 设置初始金币
        self.player.gold = 50
        assert self.player.gold == 50

        # 测试增加金币
        self.player.earn_gold(30)
        assert self.player.gold == 80

        # 测试减少金币
        self.player.spend_gold(30)
        assert self.player.gold == 50

    def test_player_spend_gold(self):
        """测试花费金币"""
        # 设置初始金币
        self.player.gold = 50
        
        # 测试足够金币
        result = self.player.spend_gold(30)
        assert result is True
        assert self.player.gold == 20

        # 测试金币不足
        self.player.gold = 10
        result = self.player.spend_gold(30)
        assert result is False
        assert self.player.gold == 10

    def test_player_inventory_limit(self):
        """测试背包限制"""
        # 设置较小的背包容量以便测试
        self.player.max_inventory_size = 2
        
        # 添加物品直到背包满
        item1 = Item("物品1", "第一个物品")
        item2 = Item("物品2", "第二个物品")
        
        assert self.player.add_item(item1) is True
        assert self.player.add_item(item2) is True

        # 尝试添加更多物品应该失败
        item3 = Item("物品3", "第三个物品")
        assert self.player.add_item(item3) is False