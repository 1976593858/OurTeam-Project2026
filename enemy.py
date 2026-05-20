# enemy.py
# ================================================
# 敌人模块
# ================================================

from item import Item


class Enemy:
    """敌人类（战斗目标）"""

    def __init__(
        self,
        name: str,
        description: str,
        health: int,
        attack: int,
        drop_item: Item = None,
    ):
        self.name = name
        self.description = description
        self.health = health
        self.max_health = health
        self.attack = attack
        self.drop_item = drop_item

    def take_damage(self, damage: int) -> int:
        """受到伤害，返回实际受到的伤害值"""
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage

    def is_alive(self) -> bool:
        """检查敌人是否存活"""
        return self.health > 0
