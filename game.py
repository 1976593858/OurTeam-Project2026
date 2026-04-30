# game.py
# ================================================
# 游戏主模块
# ================================================

from item import Item
from room import Room
from player import Player

class Game:
    """游戏主控类"""
    player: Player          # ← 类级别类型声明（Pylance 推荐写法，彻底解决 Optional 问题）

    def __init__(self):
        self._setup_world()  # 在这里真正初始化 player

    def _setup_world(self):
        """MVP 世界地图：5 个房间 + 2 件物品"""
        foyer = Room("门厅", "你站在一栋古老宅邸的宏伟门厅里，地板上布满灰尘。")
        living_room = Room("客厅", "温馨的客厅，壁炉正在燃烧，还有一张舒适的沙发。")
        kitchen = Room("厨房", "厨房里弥漫着陈年香料的味道，锅碗瓢盆挂在天花板上。")
        bedroom = Room("卧室", "尘埃覆盖的卧室，中央摆着一张大床。")
        garden = Room("花园", "外面是杂草丛生的花园，奇异的花朵正在绽放。")

        # 连接出口
        foyer.add_exit("north", living_room)
        living_room.add_exit("south", foyer)
        foyer.add_exit("east", kitchen)
        kitchen.add_exit("west", foyer)
        living_room.add_exit("west", bedroom)
        bedroom.add_exit("east", living_room)
        kitchen.add_exit("east", garden)
        garden.add_exit("west", kitchen)

        # 添加物品
        key = Item("钥匙", "一把生锈的旧钥匙，看起来能打开某扇门。")
        apple = Item("苹果", "一个新鲜红润的苹果，闻起来很香。")
        bedroom.add_item(key)
        kitchen.add_item(apple)

        # 创建 NPC
        merchant = NPC("商人", "一位神秘的旅行商人。")
        merchant.add_item(TradeableItem("治疗药水", "恢复 20 点生命值", 30))
        merchant.add_item(TradeableItem("魔法卷轴", "释放一道闪电", 50))
        living_room.npcs.append(merchant)

        self.player = Player(foyer)   # ← 这里真正赋值

    # ------------------- 辅助显示 -------------------
    def _print_room(self):
        room = self.player.current_room
        print(f"\n=== {room.name} ===")
        print(room.description)

        if room.exits:
            dir_map = {"north": "北", "south": "南", "east": "东", "west": "西"}
            # 修复Pylance类型警告，只获取存在于dir_map中的方向
            exits_list: list[str] = [dir_map[d] for d in room.exits.keys() if d in dir_map]
            exits_str = ", ".join(exits_list)
            print(f"出口：{exits_str}")

        visible_items = [item.name for item in room.items]
        if visible_items:
            print(f"你看到：{', '.join(visible_items)}")

    # ------------------- 命令处理 -------------------
    def _process_command(self, command: str):
        if not command.strip():
            return
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
            self._go(direction_map[verb])
            return
        if verb == "go":
            if noun in direction_map:
                self._go(direction_map[noun])
            else:
                print("你要去哪个方向？（north/south/east/west 或简写 n/s/e/w）")
            return
        if verb in ("look", "l"):
            self._print_room()
            return
        if verb in ("take", "get", "t"):
            if noun:
                self._take(noun)
            else:
                print("你要拿什么？")
            return
        if verb in ("inventory", "i", "inv"):
            self._show_inventory()
            return
        if verb in ("quit", "q", "exit"):
            print("感谢游玩！再见～")
            exit(0)

        print("我不明白这个命令。试试：look / l、go north / north、take 钥匙、inventory/i、quit")

    def _go(self, direction: str):
        if self.player.move(direction):
            dir_chinese = {"north": "北", "south": "南", "east": "东", "west": "西"}
            print(f"你向 {dir_chinese.get(direction, direction)} 走去。")
            self._print_room()
        else:
            print("那个方向走不通！")

    def _take(self, item_name: str):
        item = self.player.take_item(item_name)
        if item:
            print(f"你拿起了 {item.name}。")
        else:
            print(f"这里没有“{item_name}”可以拿取。")

    def _show_inventory(self):
        if not self.player.inventory:
            print("你的背包是空的。")
            return
        print("背包物品：")
        for item in self.player.inventory:
            print(f"  • {item.name} —— {item.description}")

    def play(self):
        print("=" * 50)
        print("欢迎来到《老宅探险》文字冒险游戏！")
        print("MVP 已实现 5 房间 + 拾取闭环")
        print("可用命令：look/l、go <方向> 或直接输入 north/n、take <物品>、inventory/i、quit")
        print("=" * 50)
        self._print_room()

        while True:
            try:
                cmd = input("\n> ").strip()
                self._process_command(cmd)
            except KeyboardInterrupt:
                print("\n\n游戏已退出。感谢游玩！")
                break

from typing import Optional, Dict, Any
from item import Item, Weapon, Consumable, TradeableItem
from room import Room
from player import Player
from npc import NPC

class GameEngine:
    """游戏引擎（核心业务逻辑）"""
    
    def __init__(self):
        self.players: Dict[str, Player] = {}  # 多玩家支持
        self.npcs: Dict[str, NPC] = {}        # NPC 注册表
    
    def create_player(self, player_id: str, starting_room: Room) -> Player:
        """创建新玩家"""
        player = Player(starting_room)
        self.players[player_id] = player
        return player
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """获取玩家"""
        return self.players.get(player_id)
    
    def trade_item(
        self,
        player: Player,
        item: TradeableItem,
        npc_or_shop: NPC,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        玩家与 NPC/商店交易物品
        
        Returns:
            dict: 交易结果，包含 success、message、item、quantity、remaining_gold
        """
        # 验证数量
        if quantity <= 0:
            return {
                "success": False,
                "message": "无效数量"
            }
        
        # 检查 NPC 是否有足够物品
        if not npc_or_shop.has_item(item.name, quantity):
            return {
                "success": False,
                "message": "物品不存在"
            }
        
        # 计算总价
        total_price = item.price * quantity
        
        # 检查玩家金币
        if player.gold < total_price:
            return {
                "success": False,
                "message": "金币不足"
            }
        
        # 检查背包空间
        if len(player.inventory) + quantity > player.max_inventory_size:
            return {
                "success": False,
                "message": "背包已满"
            }
        
        # 执行交易
        player.spend_gold(total_price)
        npc_or_shop.remove_item(item.name, quantity)
        
        # 添加物品到玩家背包
        for _ in range(quantity):
            player.add_item(item)
        
        return {
            "success": True,
            "message": f"成功购买 {quantity} 个 {item.name}",
            "item": item,
            "quantity": quantity,
            "remaining_gold": player.gold
        }

class Game:
    """游戏主控类（命令行界面）"""
    player: Player          # ← 类级别类型声明（Pylance 推荐写法，彻底解决 Optional 问题）

    def __init__(self):
        self._setup_world()  # 在这里真正初始化 player

    def _setup_world(self):
        """MVP 世界地图：5 个房间 + 2 件物品"""
        foyer = Room("门厅", "你站在一栋古老宅邸的宏伟门厅里，地板上布满灰尘。")
        living_room = Room("客厅", "温馨的客厅，壁炉正在燃烧，还有一张舒适的沙发。")
        kitchen = Room("厨房", "厨房里弥漫着陈年香料的味道，锅碗瓢盆挂在天花板上。")
        bedroom = Room("卧室", "尘埃覆盖的卧室，中央摆着一张大床。")
        garden = Room("花园", "外面是杂草丛生的花园，奇异的花朵正在绽放。")

        # 连接出口
        foyer.add_exit("north", living_room)
        living_room.add_exit("south", foyer)
        foyer.add_exit("east", kitchen)
        kitchen.add_exit("west", foyer)
        living_room.add_exit("west", bedroom)
        bedroom.add_exit("east", living_room)
        kitchen.add_exit("east", garden)
        garden.add_exit("west", kitchen)

        # 添加物品
        key = Item("钥匙", "一把生锈的旧钥匙，看起来能打开某扇门。")
        apple = Item("苹果", "一个新鲜红润的苹果，闻起来很香。")
        bedroom.add_item(key)
        kitchen.add_item(apple)

        # 创建 NPC
        merchant = NPC("商人", "一位神秘的旅行商人。")
        merchant.add_item(TradeableItem("治疗药水", "恢复 20 点生命值", 30))
        merchant.add_item(TradeableItem("魔法卷轴", "释放一道闪电", 50))
        living_room.npcs.append(merchant)

        self.player = Player(foyer)   # ← 这里真正赋值

    # ------------------- 辅助显示 -------------------
    def _print_room(self):
        room = self.player.current_room
        print(f"\n=== {room.name} ===")
        print(room.description)

        if room.exits:
            dir_map = {"north": "北", "south": "南", "east": "东", "west": "西"}
            # 修复Pylance类型警告，只获取存在于dir_map中的方向
            exits_list: list[str] = [dir_map[d] for d in room.exits.keys() if d in dir_map]
            exits_str = ", ".join(exits_list)
            print(f"出口：{exits_str}")

        visible_items = [item.name for item in room.items]
        if visible_items:
            print(f"你看到：{', '.join(visible_items)}")

    # ------------------- 命令处理 -------------------
    def _process_command(self, command: str):
        if not command.strip():
            return
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
            self._go(direction_map[verb])
            return
        if verb == "go":
            if noun in direction_map:
                self._go(direction_map[noun])
            else:
                print("你要去哪个方向？（north/south/east/west 或简写 n/s/e/w）")
            return
        if verb in ("look", "l"):
            self._print_room()
            return
        if verb in ("take", "get", "t"):
            if noun:
                self._take(noun)
            else:
                print("你要拿什么？")
            return
        if verb in ("inventory", "i", "inv"):
            self._show_inventory()
            return
        if verb in ("quit", "q", "exit"):
            print("感谢游玩！再见～")
            exit(0)

        print("我不明白这个命令。试试：look / l、go north / north、take 钥匙、inventory/i、quit")

    def _go(self, direction: str):
        if self.player.move(direction):
            dir_chinese = {"north": "北", "south": "南", "east": "东", "west": "西"}
            print(f"你向 {dir_chinese.get(direction, direction)} 走去。")
            self._print_room()
        else:
            print("那个方向走不通！")

    def _take(self, item_name: str):
        item = self.player.take_item(item_name)
        if item:
            print(f"你拿起了 {item.name}。")
        else:
            print(f"这里没有“{item_name}”可以拿取。")

    def _show_inventory(self):
        if not self.player.inventory:
            print("你的背包是空的。")
            return
        print("背包物品：")
        for item in self.player.inventory:
            print(f"  • {item.name} —— {item.description}")

    def play(self):
        print("=" * 50)
        print("欢迎来到《老宅探险》文字冒险游戏！")
        print("MVP 已实现 5 房间 + 拾取闭环")
        print("可用命令：look/l、go <方向> 或直接输入 north/n、take <物品>、inventory/i、quit")
        print("=" * 50)
        self._print_room()

        while True:
            try:
                cmd = input("\n> ").strip()
                self._process_command(cmd)
            except KeyboardInterrupt:
                print("\n\n游戏已退出。感谢游玩！")
                break