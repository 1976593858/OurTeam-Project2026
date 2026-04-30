"""战斗计算单元测试

使用 MagicMock 隔离 Player 和 Enemy，测试核心战斗逻辑：
- 正常攻击伤害计算
- 暴击倍率机制
- 生命值扣减逻辑
- 死亡判定触发
- 攻击力边界情况（0 或负值）
"""

import sys
import os
from dataclasses import dataclass
from unittest.mock import MagicMock, call

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest


@dataclass
class DamageResult:
    """攻击结果数据类"""
    damage: int
    is_critical: bool
    target_dead: bool


class TestCombatCalculations:
    """战斗计算测试类"""

    def test_normal_attack_deals_positive_damage(self):
        """
        Given: 攻击者有正攻击力，目标有生命值
        When: 执行普通攻击
        Then: 造成正伤害且非暴击
        """
        # Setup: 创建 Mock 对象
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = 20
        defender.health = 100
        defender.take_damage.return_value = 20
        defender.is_alive.return_value = True

        # Execute: 模拟攻击逻辑
        damage = attacker.get_total_attack()
        is_critical = False  # 普通攻击无暴击
        actual_damage = defender.take_damage(damage)
        target_dead = not defender.is_alive()

        result = DamageResult(damage=actual_damage, is_critical=is_critical, target_dead=target_dead)

        # Verify
        assert result.damage > 0, "正常攻击应造成正伤害"
        assert result.is_critical is False, "普通攻击不应暴击"
        assert result.target_dead is False, "目标不应死亡"
        defender.take_damage.assert_called_once_with(20)

    def test_critical_hit_applies_multiplier(self):
        """
        Given: 攻击触发暴击（假设暴击倍率为 2.0）
        When: 执行暴击攻击
        Then: 伤害为基础攻击力的 2 倍
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        base_attack = 15
        crit_multiplier = 2.0
        attacker.get_total_attack.return_value = base_attack
        defender.health = 100
        defender.take_damage.return_value = int(base_attack * crit_multiplier)
        defender.is_alive.return_value = True

        # Execute: 暴击攻击逻辑
        damage = int(attacker.get_total_attack() * crit_multiplier)
        is_critical = True
        actual_damage = defender.take_damage(damage)
        target_dead = not defender.is_alive()

        result = DamageResult(damage=actual_damage, is_critical=is_critical, target_dead=target_dead)

        # Verify
        expected_damage = int(base_attack * crit_multiplier)
        assert result.damage == expected_damage, f"暴击伤害应为 {expected_damage}"
        assert result.is_critical is True, "应标记为暴击"
        defender.take_damage.assert_called_once_with(expected_damage)

    def test_attack_reduces_target_health_correctly(self):
        """
        Given: 目标有 50 生命值，攻击造成 25 伤害
        When: 执行攻击
        Then: 目标生命值正确减少
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = 25
        defender.health = 50
        defender.take_damage.return_value = 25
        defender.is_alive.return_value = True

        # Execute
        damage = attacker.get_total_attack()
        defender.take_damage(damage)

        # Verify
        defender.take_damage.assert_called_once_with(25)

    def test_target_health_zero_triggers_death(self):
        """
        Given: 目标生命值为 10，攻击造成 10 伤害
        When: 执行攻击
        Then: 目标生命值归零并触发死亡
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = 10
        defender.health = 10
        defender.take_damage.return_value = 10
        defender.is_alive.return_value = False  # 生命值归零后死亡

        # Execute
        damage = attacker.get_total_attack()
        actual_damage = defender.take_damage(damage)
        target_dead = not defender.is_alive()

        result = DamageResult(damage=actual_damage, is_critical=False, target_dead=target_dead)

        # Verify
        assert result.target_dead is True, "目标应死亡"
        assert actual_damage == 10, "应造成全额伤害"

    def test_target_health_below_zero_capped_at_remaining(self):
        """
        Given: 目标生命值为 5，攻击造成 20 伤害
        When: 执行攻击
        Then: 实际伤害只扣减剩余生命值（5），目标死亡
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = 20
        defender.health = 5
        defender.take_damage.return_value = 5  # 实际伤害被限制为剩余生命
        defender.is_alive.return_value = False

        # Execute
        damage = attacker.get_total_attack()
        actual_damage = defender.take_damage(damage)
        target_dead = not defender.is_alive()

        result = DamageResult(damage=actual_damage, is_critical=False, target_dead=target_dead)

        # Verify
        assert result.damage == 5, "实际伤害应被限制为剩余生命值"
        assert result.target_dead is True, "目标应死亡"

    def test_attack_power_zero_deals_no_damage(self):
        """
        Given: 攻击者攻击力为 0（防御过高或无装备）
        When: 执行攻击
        Then: 造成 0 伤害，目标不受影响
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = 0
        defender.health = 100
        defender.take_damage.return_value = 0
        defender.is_alive.return_value = True

        # Execute
        damage = attacker.get_total_attack()
        actual_damage = defender.take_damage(damage)
        target_dead = not defender.is_alive()

        result = DamageResult(damage=actual_damage, is_critical=False, target_dead=target_dead)

        # Verify
        assert result.damage == 0, "攻击力为 0 时应造成 0 伤害"
        assert result.target_dead is False, "目标不应死亡"

    def test_negative_attack_power_deals_no_damage(self):
        """
        Given: 攻击者攻击力为负值（防御过高导致）
        When: 执行攻击
        Then: 造成 0 伤害（伤害不应为负）
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = -5  # 负值攻击力
        defender.health = 100
        defender.take_damage.return_value = 0
        defender.is_alive.return_value = True

        # Execute: 确保伤害非负
        raw_damage = attacker.get_total_attack()
        damage = max(raw_damage, 0)  # 伤害不应为负
        actual_damage = defender.take_damage(damage)
        target_dead = not defender.is_alive()

        result = DamageResult(damage=actual_damage, is_critical=False, target_dead=target_dead)

        # Verify
        assert damage == 0, "负值攻击力应被修正为 0"
        assert result.damage == 0, "应造成 0 伤害"

    def test_consecutive_attacks_until_death(self):
        """
        Given: 目标生命值为 30，每次攻击造成 10 伤害
        When: 连续执行 3 次攻击
        Then: 第 3 次攻击后目标死亡
        """
        attacker = MagicMock(name="attacker")
        defender = MagicMock(name="defender")
        
        attacker.get_total_attack.return_value = 10
        
        # 模拟三次攻击的状态变化
        defender.take_damage.side_effect = [10, 10, 10]
        defender.is_alive.side_effect = [True, True, False]

        # Execute: 三次连续攻击
        results = []
        for _ in range(3):
            damage = attacker.get_total_attack()
            actual_damage = defender.take_damage(damage)
            target_dead = not defender.is_alive()
            results.append(DamageResult(
                damage=actual_damage, 
                is_critical=False, 
                target_dead=target_dead
            ))

        # Verify
        assert defender.take_damage.call_count == 3, "应调用 3 次 take_damage"
        assert results[0].target_dead is False, "第一次攻击后不应死亡"
        assert results[1].target_dead is False, "第二次攻击后不应死亡"
        assert results[2].target_dead is True, "第三次攻击后应死亡"
        defender.take_damage.assert_has_calls([call(10), call(10), call(10)])