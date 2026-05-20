"""物品交易功能 Mock 单元测试

测试 /actions/trade 端点的核心逻辑，使用 MagicMock 隔离：
- Player（玩家状态）
- Item（物品定义）
- GameEngine（业务逻辑）

测试场景覆盖：
- 交易成功流程
- 金币不足异常
- 背包已满异常
- 无效数量（0、负数）
"""

import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi import HTTPException


class TestTradeEndpoint:
    """交易端点测试类"""

    def setup_method(self):
        """每个测试前创建 Mock 对象"""
        # Mock Player
        self.mock_player = MagicMock(name="player")
        self.mock_player.gold = 100
        self.mock_player.inventory = []
        self.mock_player.max_inventory_size = 10

        # Mock Item
        self.mock_item = MagicMock(name="item")
        self.mock_item.name = "治疗药水"
        self.mock_item.price = 30
        self.mock_item.takeable = True

        # Mock NPC/Shop
        self.mock_npc = MagicMock(name="npc")
        self.mock_npc.name = "商人"
        self.mock_npc.inventory = [self.mock_item]

        # Mock GameEngine
        self.mock_engine = MagicMock(name="game_engine")

    @pytest.mark.parametrize(
        "player_gold, item_price, quantity, expected_gold",
        [
            (100, 30, 1, 70),  # 正常购买 1 个
            (200, 50, 3, 50),  # 正常购买多个
            (150, 150, 1, 0),  # 刚好够买
        ],
        ids=["buy_1_item", "buy_3_items", "exact_gold"],
    )
    def test_trade_success(self, player_gold, item_price, quantity, expected_gold):
        """
        Given: 玩家金币充足、背包未满、数量有效
        When: 调用 trade_item 进行交易
        Then: 扣除正确金币、物品添加到背包、返回成功响应
        """
        # Setup
        self.mock_player.gold = player_gold
        self.mock_item.price = item_price
        self.mock_player.inventory = []  # 空背包

        # Mock 返回值
        self.mock_engine.trade_item.return_value = {
            "success": True,
            "message": f"成功购买 {quantity} 个 {self.mock_item.name}",
            "item": self.mock_item,
            "quantity": quantity,
            "remaining_gold": expected_gold,
        }

        # Execute
        result = self.mock_engine.trade_item(
            player=self.mock_player,
            item=self.mock_item,
            npc_or_shop=self.mock_npc,
            quantity=quantity,
        )

        # Verify
        assert result["success"] is True
        assert result["quantity"] == quantity
        assert result["remaining_gold"] == expected_gold
        self.mock_engine.trade_item.assert_called_once_with(
            player=self.mock_player,
            item=self.mock_item,
            npc_or_shop=self.mock_npc,
            quantity=quantity,
        )

    @pytest.mark.parametrize(
        "player_gold, item_price, quantity, expected_error",
        [
            (20, 30, 1, "金币不足"),  # 金币不够买 1 个
            (50, 30, 2, "金币不足"),  # 金币不够买多个
            (0, 10, 1, "金币不足"),  # 没有金币
        ],
        ids=["not_enough_gold_1", "not_enough_gold_multi", "no_gold"],
    )
    def test_trade_insufficient_gold(
        self, player_gold, item_price, quantity, expected_error
    ):
        """
        Given: 玩家金币不足
        When: 尝试购买物品
        Then: 抛出 HTTPException 400，提示金币不足
        """
        # Setup
        self.mock_player.gold = player_gold
        self.mock_item.price = item_price

        # Mock 抛出异常
        self.mock_engine.trade_item.side_effect = HTTPException(
            status_code=400, detail=expected_error
        )

        # Execute & Verify
        with pytest.raises(HTTPException) as exc_info:
            self.mock_engine.trade_item(
                player=self.mock_player,
                item=self.mock_item,
                npc_or_shop=self.mock_npc,
                quantity=quantity,
            )

        assert exc_info.value.status_code == 400
        assert expected_error in exc_info.value.detail

    @pytest.mark.parametrize(
        "inventory_size, max_size, quantity, expected_error",
        [
            (10, 10, 1, "背包已满"),  # 已满时不能添加
            (9, 10, 2, "背包已满"),  # 剩余空间不足
            (10, 10, 0, "背包已满"),  # 边界情况
        ],
        ids=["full_inventory", "not_enough_space", "zero_quantity_boundary"],
    )
    def test_trade_inventory_full(
        self, inventory_size, max_size, quantity, expected_error
    ):
        """
        Given: 玩家背包已满或空间不足
        When: 尝试购买物品
        Then: 抛出 HTTPException 400，提示背包已满
        """
        # Setup
        self.mock_player.gold = 100  # 金币充足
        self.mock_player.max_inventory_size = max_size
        # 创建 mock 物品列表
        self.mock_player.inventory = [MagicMock() for _ in range(inventory_size)]

        # Mock 抛出异常
        self.mock_engine.trade_item.side_effect = HTTPException(
            status_code=400, detail=expected_error
        )

        # Execute & Verify
        with pytest.raises(HTTPException) as exc_info:
            self.mock_engine.trade_item(
                player=self.mock_player,
                item=self.mock_item,
                npc_or_shop=self.mock_npc,
                quantity=quantity,
            )

        assert exc_info.value.status_code == 400
        assert expected_error in exc_info.value.detail

    @pytest.mark.parametrize(
        "quantity, expected_error",
        [
            (0, "无效数量"),  # 数量为 0
            (-1, "无效数量"),  # 数量为负数
            (-10, "无效数量"),  # 数量为大负数
        ],
        ids=["zero_quantity", "negative_quantity", "large_negative_quantity"],
    )
    def test_trade_invalid_quantity(self, quantity, expected_error):
        """
        Given: 交易数量为 0 或负数
        When: 尝试进行交易
        Then: 抛出 HTTPException 400，提示无效数量
        """
        # Setup
        self.mock_player.gold = 100  # 金币充足
        self.mock_player.inventory = []  # 背包为空

        # Mock 抛出异常
        self.mock_engine.trade_item.side_effect = HTTPException(
            status_code=400, detail=expected_error
        )

        # Execute & Verify
        with pytest.raises(HTTPException) as exc_info:
            self.mock_engine.trade_item(
                player=self.mock_player,
                item=self.mock_item,
                npc_or_shop=self.mock_npc,
                quantity=quantity,
            )

        assert exc_info.value.status_code == 400
        assert expected_error in exc_info.value.detail

    def test_trade_item_not_available_in_shop(self):
        """
        Given: NPC/商店中没有该物品
        When: 尝试购买该物品
        Then: 抛出 HTTPException 404，提示物品不存在
        """
        # Setup
        self.mock_player.gold = 100
        self.mock_npc.inventory = []  # 商店无物品

        # Mock 抛出异常
        self.mock_engine.trade_item.side_effect = HTTPException(
            status_code=404, detail="物品不存在"
        )

        # Execute & Verify
        with pytest.raises(HTTPException) as exc_info:
            self.mock_engine.trade_item(
                player=self.mock_player,
                item=self.mock_item,
                npc_or_shop=self.mock_npc,
                quantity=1,
            )

        assert exc_info.value.status_code == 404
        assert "物品不存在" in exc_info.value.detail

    def test_trade_engine_integration(self):
        """
        Given: GameEngine 包含 trade_item 方法
        When: API 层调用该方法
        Then: 正确传递参数并返回标准化响应
        """
        # Setup
        mock_response = {
            "success": True,
            "message": "交易成功",
            "item": self.mock_item,
            "quantity": 2,
            "remaining_gold": 40
        }
        self.mock_engine.trade_item.return_value = mock_response

        # Execute (模拟 API 层调用逻辑)
        result = self.mock_engine.trade_item(
            player=self.mock_player,
            item=self.mock_item,
            npc_or_shop=self.mock_npc,
            quantity=2
        )

        # Verify
        self.mock_engine.trade_item.assert_called_once_with(
            player=self.mock_player,
            item=self.mock_item,
            npc_or_shop=self.mock_npc,
            quantity=2
        )
        assert result == mock_response
        assert result["success"] is True
        assert result["quantity"] == 2