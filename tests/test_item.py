import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from item import Item


class TestItem:
    def test_item_creation(self):
        """物品应能正确创建"""
        sword = Item("剑", "一把锋利的剑")
        assert sword.name == "剑"
        assert sword.description == "一把锋利的剑"

    def test_item_str_representation(self):
        """物品的字符串表示不应为空"""
        item = Item("钥匙", "神秘的钥匙")
        assert str(item) != ""