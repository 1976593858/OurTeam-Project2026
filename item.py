# item.py
# ================================================
# 物品模块（独立、可复用）
# ================================================


class Item:
    """物品类（可拾取/描述）"""

    def __init__(self, name: str, description: str, takeable: bool = True):
        self.name = name  # 原样保存（支持中文）
        self.description = description
        self.takeable = takeable


class Weapon(Item):
    """武器类（继承自物品，增加攻击力属性）"""

    def __init__(
        self, name: str, description: str, attack_power: int, takeable: bool = True
    ):
        super().__init__(name, description, takeable)
        self.attack_power = attack_power


class Consumable(Item):
    """消耗品类（继承自物品，增加恢复效果）"""

    def __init__(
        self, name: str, description: str, heal_amount: int, takeable: bool = True
    ):
        super().__init__(name, description, takeable)
        self.heal_amount = heal_amount


class TradeableItem(Item):
    """可交易物品类（继承自物品，增加价格属性）"""

    def __init__(self, name: str, description: str, price: int, takeable: bool = True):
        super().__init__(name, description, takeable)
        self.price = price