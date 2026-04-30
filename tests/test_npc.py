import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from npc import NPC
from item import Item, TradeableItem


class TestNPC:
    def setup_method(self):
        """每个测试前创建新的NPC实例"""
        self.npc = NPC("测试NPC", "一个用于测试的NPC")

    def test_npc_initialization(self):
        """测试NPC初始化"""
        assert self.npc.name == "测试NPC"
        assert self.npc.description == "一个用于测试的NPC"
        assert self.npc.inventory == []

    def test_add_item(self):
        """测试添加物品到NPC"""
        item = Item("测试物品", "一个测试物品")
        self.npc.add_item(item)
        
        assert len(self.npc.inventory) == 1
        assert self.npc.inventory[0] == item

    def test_remove_item_success(self):
        """测试成功移除物品"""
        item = TradeableItem("测试物品", "一个测试物品", 10)
        self.npc.add_item(item)
        
        result = self.npc.remove_item("测试物品", 1)
        
        assert result is True
        assert len(self.npc.inventory) == 0

    def test_remove_item_failure(self):
        """测试移除不存在物品的失败情况"""
        result = self.npc.remove_item("不存在的物品", 1)
        
        assert result is False
        assert len(self.npc.inventory) == 0

    def test_has_item_with_enough_quantity(self):
        """测试拥有足够数量物品的情况"""
        item1 = TradeableItem("测试物品", "一个测试物品", 10)
        item2 = TradeableItem("测试物品", "另一个测试物品", 10)
        self.npc.add_item(item1)
        self.npc.add_item(item2)
        
        # 检查是否有2个物品
        assert self.npc.has_item("测试物品", 2) is True
        
        # 检查是否有1个物品
        assert self.npc.has_item("测试物品", 1) is True

    def test_has_item_without_enough_quantity(self):
        """测试没有足够数量物品的情况"""
        item = TradeableItem("测试物品", "一个测试物品", 10)
        self.npc.add_item(item)
        
        # 检查是否有2个物品，但实际上只有1个
        assert self.npc.has_item("测试物品", 2) is False

    def test_has_item_with_no_matching_items(self):
        """测试没有匹配物品的情况"""
        assert self.npc.has_item("不存在的物品", 1) is False

    def test_get_item_price_for_tradeable_item(self):
        """测试获取可交易物品的价格"""
        item = TradeableItem("测试物品", "一个测试物品", 25)
        self.npc.add_item(item)
        
        price = self.npc.get_item_price("测试物品")
        
        assert price == 25

    def test_get_item_price_for_non_tradeable_item(self):
        """测试获取非可交易物品的价格"""
        item = Item("测试物品", "一个测试物品")
        self.npc.add_item(item)
        
        price = self.npc.get_item_price("测试物品")
        
        assert price == 0

    def test_get_item_price_for_nonexistent_item(self):
        """测试获取不存在物品的价格"""
        price = self.npc.get_item_price("不存在的物品")
        
        assert price == 0