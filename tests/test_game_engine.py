import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game import GameEngine
from player import Player
from room import Room
from item import TradeableItem
from npc import NPC


class TestGameEngine:
    def setup_method(self):
        """每个测试前创建新的 GameEngine 实例"""
        self.engine = GameEngine()

    def test_create_player(self):
        """测试创建玩家"""
        room = Room("测试房间", "一个测试房间")
        player = self.engine.create_player("test_player", room)
        
        assert isinstance(player, Player)
        assert self.engine.get_player("test_player") == player

    def test_get_nonexistent_player(self):
        """测试获取不存在的玩家"""
        player = self.engine.get_player("nonexistent_player")
        
        assert player is None

    def test_trade_item_with_insufficient_gold(self):
        """测试金币不足时的交易"""
        # 创建房间和玩家
        room = Room("测试房间", "一个测试房间")
        player = self.engine.create_player("test_player", room)
        player.gold = 10  # 只给玩家10金币
        
        # 创建NPC和物品
        npc = NPC("商人", "一个商人")
        expensive_item = TradeableItem("昂贵物品", "非常贵的物品", 100)  # 需要100金币
        npc.add_item(expensive_item)
        room.npcs.append(npc)
        
        # 尝试交易 - 应该失败，因为金币不足
        result = self.engine.trade_item(player, expensive_item, npc, 1)
        
        assert result["success"] is False
        assert "金币不足" in result["message"]

    def test_trade_item_with_invalid_quantity(self):
        """测试无效数量的交易"""
        # 创建房间和玩家
        room = Room("测试房间", "一个测试房间")
        player = self.engine.create_player("test_player", room)
        
        # 创建NPC和物品
        npc = NPC("商人", "一个商人")
        item = TradeableItem("普通物品", "一个普通物品", 10)
        npc.add_item(item)
        room.npcs.append(npc)
        
        # 尝试交易 - 数量为0，应该失败
        result = self.engine.trade_item(player, item, npc, 0)
        
        assert result["success"] is False
        assert "无效数量" in result["message"]
        
        # 尝试交易 - 数量为负数，应该失败
        result = self.engine.trade_item(player, item, npc, -1)
        
        assert result["success"] is False
        assert "无效数量" in result["message"]

    def test_trade_item_with_full_inventory(self):
        """测试背包满了的情况下的交易"""
        # 创建房间和玩家
        room = Room("测试房间", "一个测试房间")
        player = self.engine.create_player("test_player", room)
        player.gold = 100
        player.max_inventory_size = 0  # 设置背包容量为0，这样任何物品都会导致背包满
        
        # 创建NPC和物品
        npc = NPC("商人", "一个商人")
        item = TradeableItem("普通物品", "一个普通物品", 10)
        npc.add_item(item)
        room.npcs.append(npc)
        
        # 尝试交易 - 应该失败，因为背包已满
        result = self.engine.trade_item(player, item, npc, 1)
        
        assert result["success"] is False
        assert "背包已满" in result["message"]

    def test_trade_item_with_insufficient_stock(self):
        """测试NPC库存不足时的交易"""
        # 创建房间和玩家
        room = Room("测试房间", "一个测试房间")
        player = self.engine.create_player("test_player", room)
        player.gold = 100
        
        # 创建NPC和物品，只添加1个
        npc = NPC("商人", "一个商人")
        item = TradeableItem("普通物品", "一个普通物品", 10)
        npc.add_item(item)
        room.npcs.append(npc)
        
        # 尝试购买2个 - 应该失败，因为NPC只有1个
        result = self.engine.trade_item(player, item, npc, 2)
        
        assert result["success"] is False
        assert "物品不存在" in result["message"]