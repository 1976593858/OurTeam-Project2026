# player.py
# ================================================
# 玩家模块（依赖 Room）
# ================================================

from room import Room
from item import Weapon


class Player:
    """玩家类（当前位置 + 背包 + 战斗属性）"""

    def __init__(self, starting_room: Room, health: int = 100, attack: int = 10, gold: int = 0, max_inventory_size: int = 10):
        self.current_room = starting_room
        self.inventory = []
        self.health = health
        self.max_health = health
        self.attack = attack
        self.equipped_weapon = None
        self.gold = gold  # 添加金币属性
        self.max_inventory_size = max_inventory_size  # 添加背包最大容量

    def move(self, direction: str) -> bool:
        """移动到指定方向"""
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
            return True
        return False

    def take_item(self, item_name: str):
        """拾取物品（从房间移除，放入背包）"""
        item_name_lower = item_name.lower()
        for item in list(self.current_room.items):  # 复制列表避免遍历时修改
            if item.name.lower() == item_name_lower and item.takeable:
                # 检查背包是否已满
                if len(self.inventory) >= self.max_inventory_size:
                    return None
                self.inventory.append(item)
                self.current_room.items.remove(item)
                return item
        return None

    def add_item(self, item):
        """添加物品到背包（通常用于交易或制作）"""
        if len(self.inventory) < self.max_inventory_size:
            self.inventory.append(item)
            return True
        return False

    def equip_weapon(self, weapon_name: str) -> bool:
        """装备武器"""
        for item in self.inventory:
            if isinstance(item, Weapon) and item.name.lower() == weapon_name.lower():
                self.equipped_weapon = item
                return True
        return False

    def get_total_attack(self) -> int:
        """获取总攻击力（基础攻击 + 武器加成）"""
        total = self.attack
        if self.equipped_weapon:
            total += self.equipped_weapon.attack_power
        return total

    def take_damage(self, damage: int) -> int:
        """受到伤害，返回实际受到的伤害值"""
        actual_damage = min(damage, self.health)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount: int) -> int:
        """恢复生命值，返回实际恢复量"""
        actual_heal = min(amount, self.max_health - self.health)
        self.health += actual_heal
        return actual_heal

    def is_alive(self) -> bool:
        """检查玩家是否存活"""
        return self.health > 0

    def spend_gold(self, amount: int) -> bool:
        """花费金币"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def earn_gold(self, amount: int):
        """获得金币"""
        self.gold += amount