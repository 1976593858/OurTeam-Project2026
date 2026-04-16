import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from unittest.mock import patch
from game import Game
from item import Item


class TestGameMock:
    def setup_method(self):
        """每个测试前创建新的 Game 实例"""
        self.game = Game()

    def test_look_command_returns_output(self, capsys):
        """look 指令应该打印当前房间信息"""
        self.game._process_command("look")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_move_north_from_foyer(self, capsys):
        """在门厅执行 north 指令应该成功移动到客厅"""
        self.game._process_command("north")
        assert self.game.player.current_room.name == "客厅"

    def test_move_invalid_direction(self, capsys):
        """向没有出口的方向移动应该提示走不通"""
        self.game._process_command("north")  # 先到客厅
        self.game._process_command("north")  # 客厅没有 north 出口
        captured = capsys.readouterr()
        assert "走不通" in captured.out

    def test_take_item_in_room(self, capsys):
        """拾取房间内存在的物品应该成功"""
        # 先走到厨房（东边），厨房里有苹果
        self.game._process_command("east")
        self.game._process_command("take 苹果")
        captured = capsys.readouterr()
        assert "苹果" in captured.out

    def test_inventory_empty_at_start(self, capsys):
        """游戏开始时背包应为空"""
        self.game._process_command("inventory")
        captured = capsys.readouterr()
        assert "空" in captured.out

    @patch('builtins.exit')
    def test_quit_command(self, mock_exit, capsys):
        """quit 指令应该触发退出"""
        self.game._process_command("quit")
        mock_exit.assert_called_once_with(0)