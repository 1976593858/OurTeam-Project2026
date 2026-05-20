"""敌人模块单元测试"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from enemy import Enemy
from item import Item


class TestEnemy:
    """敌人类测试"""

    def setup_method(self):
        self.item = Item("金币", "闪闪发光的金币")
        self.enemy = Enemy("哥布林", "一只绿色的哥布林", 50, 10, self.item)

    def test_enemy_initialization(self):
        """测试敌人初始化"""
        assert self.enemy.name == "哥布林"
        assert self.enemy.health == 50
        assert self.enemy.max_health == 50
        assert self.enemy.attack == 10
        assert self.enemy.drop_item == self.item

    def test_enemy_take_damage(self):
        """测试敌人受到伤害"""
        damage = self.enemy.take_damage(20)
        assert damage == 20
        assert self.enemy.health == 30

    def test_enemy_take_excess_damage(self):
        """测试敌人受到超过生命值的伤害"""
        damage = self.enemy.take_damage(100)
        assert damage == 50  # 只扣剩余生命值
        assert self.enemy.health == 0

    def test_enemy_is_alive(self):
        """测试敌人存活状态"""
        assert self.enemy.is_alive() is True
        self.enemy.take_damage(50)
        assert self.enemy.is_alive() is False
