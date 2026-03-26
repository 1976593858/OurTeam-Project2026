# player.py
# ================================================
# 玩家模块（依赖 Room）
# ================================================

from room import Room

class Player:
    """玩家类（当前位置 + 背包）"""
    def __init__(self, starting_room: Room):
        self.current_room = starting_room
        self.inventory = []

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
                self.inventory.append(item)
                self.current_room.items.remove(item)
                return item
        return None