import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game import Game


def test_main_game_can_be_created():
    """测试可以创建游戏实例"""
    game = Game()
    assert game is not None


@patch('builtins.input', side_effect=['look', 'quit'])
@patch('builtins.exit')
def test_main_game_play(mock_exit, mock_input):
    """测试游戏的基本运行流程"""
    game = Game()
    # 捕获异常，因为游戏正常退出时会调用exit()
    try:
        game.play()
    except SystemExit:
        # 游戏结束时会调用exit，这是正常的
        pass
    mock_exit.assert_called_once()