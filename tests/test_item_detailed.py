import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from item import Item, Weapon, Consumable, TradeableItem


class TestItemDetailed:
    def test_item_creation_with_default_takeable(self):
        """测试默认可拾取的物品创建"""
        item = Item("测试物品", "一个测试物品")
        
        assert item.name == "测试物品"
        assert item.description == "一个测试物品"
        assert item.takeable is True

    def test_item_creation_with_custom_takeable(self):
        """测试自定义可拾取属性的物品创建"""
        item = Item("不可拾取物品", "一个不可拾取的物品", takeable=False)
        
        assert item.name == "不可拾取物品"
        assert item.description == "一个不可拾取的物品"
        assert item.takeable is False


class TestWeapon:
    def test_weapon_creation(self):
        """测试武器创建"""
        weapon = Weapon("剑", "一把锋利的剑", 20)
        
        assert weapon.name == "剑"
        assert weapon.description == "一把锋利的剑"
        assert weapon.attack_power == 20
        assert weapon.takeable is True

    def test_weapon_creation_with_custom_takeable(self):
        """测试自定义可拾取属性的武器创建"""
        weapon = Weapon("展示武器", "仅作展示的武器", 0, takeable=False)
        
        assert weapon.name == "展示武器"
        assert weapon.description == "仅作展示的武器"
        assert weapon.attack_power == 0
        assert weapon.takeable is False


class TestConsumable:
    def test_consumable_creation(self):
        """测试消耗品创建"""
        consumable = Consumable("治疗药水", "恢复生命值", 30)
        
        assert consumable.name == "治疗药水"
        assert consumable.description == "恢复生命值"
        assert consumable.heal_amount == 30
        assert consumable.takeable is True

    def test_consumable_creation_with_custom_takeable(self):
        """测试自定义可拾取属性的消耗品创建"""
        consumable = Consumable("特殊药水", "特殊的消耗品", 50, takeable=False)
        
        assert consumable.name == "特殊药水"
        assert consumable.description == "特殊的消耗品"
        assert consumable.heal_amount == 50
        assert consumable.takeable is False


class TestTradeableItem:
    def test_tradeable_item_creation(self):
        """测试可交易物品创建"""
        item = TradeableItem("交易物品", "一个可交易的物品", 100)
        
        assert item.name == "交易物品"
        assert item.description == "一个可交易的物品"
        assert item.price == 100
        assert item.takeable is True

    def test_tradeable_item_creation_with_custom_takeable(self):
        """测试自定义可拾取属性的可交易物品创建"""
        item = TradeableItem("特殊交易物品", "特殊的可交易物品", 200, takeable=False)
        
        assert item.name == "特殊交易物品"
        assert item.description == "特殊的可交易物品"
        assert item.price == 200
        assert item.takeable is False