from room import Room
from item import Item
from player import Player

class GameEngine:
    def __init__(self):
        self.player = None
        self._setup_world()

    def _setup_world(self):
        foyer = Room("门厅", "灰尘满布的古老宅邸。")
        kitchen = Room("厨房", "有苹果的厨房。")
        foyer.add_exit("east", kitchen)
        kitchen.add_exit("west", foyer)

        apple = Item("苹果", "一个红苹果")
        kitchen.add_item(apple)

        self.player = Player(foyer)

    def move(self, direction: str) -> dict:
        self.player.move(direction)
        return self.get_state()

    def get_state(self) -> dict:
        room = self.player.current_room
        return {
            "room": room.name,
            "desc": room.description,
            "exits": list(room.exits.keys()),
            "inventory": [item.name for item in self.player.inventory]
        }