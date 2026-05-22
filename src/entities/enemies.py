from dataclasses import dataclass, field
from typing import Optional
import random


@dataclass
class Enemy:
    id: str
    name: str
    health: int
    max_health: int
    damage: int
    speed: float
    behavior: str
    is_boss: bool = False
    weak_point: Optional[str] = None
    armor: Optional[str] = None

    @property
    def alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int, hit_weak_point: bool = False) -> int:
        multiplier = 3.0 if hit_weak_point and self.weak_point else 1.0
        if self.armor and not hit_weak_point:
            amount = max(1, amount // 2)
        dealt = int(amount * multiplier)
        self.health = max(0, self.health - dealt)
        tag = f" [WEAK POINT x{multiplier:.0f}!]" if hit_weak_point else ""
        print(f"  {self.name} takes {dealt} damage{tag}. ({self.health}/{self.max_health} HP)")
        return dealt

    def attack(self) -> int:
        variance = random.randint(-2, 4)
        return max(0, self.damage + variance)

    def status_bar(self, width: int = 16) -> str:
        filled = int((self.health / self.max_health) * width)
        return f"[{'█' * filled}{'░' * (width - filled)}]"


ENEMY_TEMPLATES: dict[str, dict] = {
    "jackal":           dict(name="Jackal",              health=20,  damage=5,  speed=7.0, behavior="pack_flanker"),
    "wolf":             dict(name="Wolf",                health=45,  damage=12, speed=9.0, behavior="ambush"),
    "lion":             dict(name="Lion",                health=120, damage=25, speed=8.0, behavior="charge_and_swipe",   is_boss=True),
    "bear":             dict(name="Bear",                health=160, damage=30, speed=5.0, behavior="berserk_when_wounded", is_boss=True),
    "philistine_archer":dict(name="Philistine Archer",   health=35,  damage=18, speed=3.0, behavior="ranged_stationary"),
    "goliath":          dict(name="Goliath of Gath",     health=500, damage=80, speed=4.0, behavior="sweep_attacks",
                             is_boss=True, weak_point="forehead", armor="bronze_full"),
    "sauls_guard":      dict(name="Saul's Guard",        health=60,  damage=20, speed=5.0, behavior="patrol"),
    "royal_scout":      dict(name="Royal Scout",         health=40,  damage=15, speed=8.0, behavior="alert_and_flee"),
    "jebusite_guard":   dict(name="Jebusite Guard",      health=70,  damage=22, speed=5.5, behavior="shield_wall"),
    "jebusite_archer":  dict(name="Jebusite Archer",     health=35,  damage=20, speed=3.0, behavior="ranged_stationary"),
    "jebusite_king":    dict(name="Jebusite King",       health=280, damage=40, speed=6.0, behavior="shield_bash",       is_boss=True),
}


def spawn(enemy_id: str) -> Enemy:
    template = ENEMY_TEMPLATES.get(enemy_id)
    if template is None:
        raise ValueError(f"Unknown enemy id: {enemy_id!r}")
    t = template.copy()
    return Enemy(
        id=enemy_id,
        max_health=t["health"],
        **t,
    )
