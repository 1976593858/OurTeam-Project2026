# room.py
# ================================================
# 房间模块（依赖 Item）
# ================================================

from item import Item

class Room:
    """房间类（描述 + 出口 + 物品）"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits = {}      # {"north": Room对象}
        self.items = []      # 当前房间的物品列表

    def add_exit(self, direction: str, target_room):
        """添加出口（支持 north/south/east/west）"""
        self.exits[direction.lower()] = target_room

    def add_item(self, item: Item):
        """放入物品"""
        self.items.append(item)