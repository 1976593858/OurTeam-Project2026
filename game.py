# game.py
# ================================================
# 游戏主模块
# ================================================

from item import Item
from room import Room
from player import Player


class Game:
    """游戏主控类"""
    player: Player

    def __init__(self):
        self._setup_world()

    def _setup_world(self):
        foyer = Room("门厅", "你站在一栋古老宅邸的宏伟门厅里，地板上布满灰尘。")
        living_room = Room("客厅", "温馨的客厅，壁炉正在燃烧，还有一张舒适的沙发。")
        kitchen = Room("厨房", "厨房里弥漫着陈年香料的味道，锅碗瓢盆挂在天花板上。")
        bedroom = Room("卧室", "尘埃覆盖的卧室，中央摆着一张大床。")
        garden = Room("花园", "外面是杂草丛生的花园，奇异的花朵正在绽放。")

        foyer.add_exit("north", living_room)
        living_room.add_exit("south", foyer)
        foyer.add_exit("east", kitchen)
        kitchen.add_exit("west", foyer)
        living_room.add_exit("west", bedroom)
        bedroom.add_exit("east", living_room)
        kitchen.add_exit("east", garden)
        garden.add_exit("west", kitchen)

        key = Item("钥匙", "一把生锈的旧钥匙，看起来能打开某扇门。")
        apple = Item("苹果", "一个新鲜红润的苹果，闻起来很香。")
        bedroom.add_item(key)
        kitchen.add_item(apple)

        self.player = Player(foyer)

    # ------------------- 辅助显示 -------------------
    def _print_room(self) -> str:
        room = self.player.current_room
        lines = [
            f"=== {room.name} ===",
            room.description
        ]
        if room.exits:
            dir_map = {"north": "北", "south": "南", "east": "东", "west": "西"}
            exits = [dir_map[d] for d in room.exits if d in dir_map]
            lines.append(f"出口：{', '.join(exits)}")
        if room.items:
            items = ", ".join(i.name for i in room.items)
            lines.append(f"你看到：{items}")
        return "\n".join(lines)

    # ------------------- 命令处理 -------------------
    def _process_command(self, command: str) -> str:
        if not command.strip():
            return ""

        parts = command.strip().lower().split(maxsplit=1)
        verb = parts[0]
        noun = parts[1] if len(parts) > 1 else ""

        direction_map = {
            "n": "north", "north": "north",
            "s": "south", "south": "south",
            "e": "east", "east": "east",
            "w": "west", "west": "west"
        }

        if verb in direction_map:
            return self._go(direction_map[verb])
        if verb == "go":
            if noun in direction_map:
                return self._go(direction_map[noun])
            return "你要去哪个方向？（north/south/east/west 或简写 n/s/e/w）"
        if verb in ("look", "l"):
            return self._print_room()
        if verb in ("take", "get", "t"):
            if noun:
                return self._take(noun)
            return "你要拿什么？"
        if verb in ("inventory", "i", "inv"):
            return self._show_inventory()
        if verb in ("quit", "q", "exit"):
            return "感谢游玩！再见～"

        return "我不明白这个命令。试试：look / l、go <方向>、take <物品>、inventory / i"

    def _go(self, direction: str) -> str:
        if self.player.move(direction):
            chinese = {"north": "北", "south": "南", "east": "东", "west": "西"}
            return f"你向 {chinese.get(direction, direction)} 走去。\n" + self._print_room()
        return "那个方向走不通！"

    def _take(self, item_name: str) -> str:
        item = self.player.take_item(item_name)
        if item:
            return f"你拿起了 {item.name}。"
        return f"这里没有“{item_name}”可以拿取。"

    def _show_inventory(self) -> str:
        if not self.player.inventory:
            return "你的背包是空的。"
        return "背包物品：\n" + "\n".join(
            f"  • {i.name} —— {i.description}" for i in self.player.inventory
        )

    def play(self):
        print("=" * 50)
        print("欢迎来到《老宅探险》文字冒险游戏！")
        print("MVP 已实现 5 房间 + 拾取闭环")
        print("可用命令：look/l、go <方向> 或直接输入 north/n、take <物品>、inventory/i、quit")
        print("=" * 50)
        print(self._print_room())

        while True:
            try:
                cmd = input("\n> ").strip()
                msg = self._process_command(cmd)
                if msg:
                    print(msg)
            except KeyboardInterrupt:
                print("\n\n游戏已退出。感谢游玩！")
                break
