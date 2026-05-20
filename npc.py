"""NPC 模块（交易功能）"""

from item import Item, TradeableItem


class NPC:
    """NPC 类（可交易的非玩家角色）"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.inventory = []

    def add_item(self, item: Item) -> None:
        """添加物品到 NPC 库存"""
        self.inventory.append(item)

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """从 NPC 库存移除物品"""
        count = 0
        items_to_remove = []
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                items_to_remove.append(item)
                count += 1
                if count >= quantity:
                    break

        if count >= quantity:
            for item in items_to_remove[:quantity]:
                self.inventory.remove(item)
            return True
        return False

    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """检查 NPC 是否有足够数量的物品"""
        count = 0
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                count += 1
                if count >= quantity:
                    return True
        return False

    def get_item_price(self, item_name: str) -> int:
        """获取物品价格"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower() and isinstance(
                item, TradeableItem
            ):
                return item.price
        return 0
