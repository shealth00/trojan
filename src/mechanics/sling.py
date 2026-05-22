"""
Sling mechanic: two-stage precision shot.
"""

import math
import random
import time
from dataclasses import dataclass
from typing import Optional

from ..entities.enemies import Enemy


@dataclass
class SlingResult:
    hit: bool
    weak_point: bool
    damage: int
    accuracy: float
    power: float
    message: str


class SlingMechanic:
    BASE_DAMAGE = 20
    SWEET_SPOT_DEGREES = 10.0

    def __init__(self, sling_tier: str = "basic"):
        tier_bonus = {"basic": 0, "leather": 5, "braided": 12, "anointed": 25}
        self.bonus_damage = tier_bonus.get(sling_tier, 0)
        self.sling_tier = sling_tier

    def _aim_phase(self, skill_level: float = 0.7) -> float:
        raw_angle = random.gauss(0, 30 * (1.0 - skill_level))
        deviation = abs(raw_angle)
        if deviation <= self.SWEET_SPOT_DEGREES:
            return 1.0
        return max(0.0, 1.0 - (deviation - self.SWEET_SPOT_DEGREES) / 90.0)

    def _power_phase(self, skill_level: float = 0.7) -> float:
        raw = random.gauss(0.85 * skill_level, 0.12)
        return max(0.0, min(1.0, raw))

    def shoot(
        self,
        target: Enemy,
        player_skill: float = 0.7,
        target_exposed: bool = False,
        stones_remaining: int = 5,
        verbose: bool = True,
    ) -> SlingResult:
        if stones_remaining <= 0:
            return SlingResult(False, False, 0, 0.0, 0.0, "No stones remaining!")

        accuracy = self._aim_phase(player_skill)
        power = self._power_phase(player_skill)

        hit = accuracy > 0.3
        perfect = accuracy >= 0.9 and power >= 0.8
        weak_point_hit = perfect and target_exposed and target.weak_point is not None

        if not hit:
            result = SlingResult(False, False, 0, accuracy, power, "The shot goes wide!")
        else:
            damage = int((self.BASE_DAMAGE + self.bonus_damage) * accuracy * power)
            if weak_point_hit:
                damage = int(damage * 3)
            target.take_damage(damage, hit_weak_point=weak_point_hit)
            msg = self._shot_message(accuracy, power, weak_point_hit)
            result = SlingResult(True, weak_point_hit, damage, accuracy, power, msg)

        if verbose:
            print(f"  [Sling] Accuracy {accuracy:.0%}  Power {power:.0%}  → {result.message}")
        return result

    def goliath_shot(self, goliath: Enemy, player_skill: float = 0.85) -> SlingResult:
        print("\n  David loads the stone, whirling the sling overhead...")
        time.sleep(0.4)
        print("  The army holds its breath...")
        time.sleep(0.4)
        print("  He releases—")
        time.sleep(0.3)
        return self.shoot(goliath, player_skill=player_skill,
                          target_exposed=True, verbose=True)

    @staticmethod
    def _shot_message(accuracy: float, power: float, weak_point: bool) -> str:
        if weak_point:
            return "PERFECT SHOT — stone strikes the forehead!"
        if accuracy >= 0.9 and power >= 0.8:
            return "Excellent shot — full impact!"
        if accuracy >= 0.7:
            return "Solid hit."
        return "Glancing blow."

    def upgrade(self, new_tier: str) -> "SlingMechanic":
        print(f"[Sling] Upgraded from '{self.sling_tier}' to '{new_tier}'")
        return SlingMechanic(new_tier)
