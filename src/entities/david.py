from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Equipment:
    weapon: str = "sling_basic"
    secondary: str = "staff"
    outfit: str = "shepherd_rags"
    instrument: Optional[str] = None


@dataclass
class Stats:
    health: int = 100
    max_health: int = 100
    speed: float = 8.0
    strength: int = 5
    defense: int = 0
    stealth: int = 6


@dataclass
class David:
    name: str = "David"
    title: str = "Son of Jesse"
    stats: Stats = field(default_factory=Stats)
    equipment: Equipment = field(default_factory=Equipment)
    faith_meter: float = 0.0
    faith_meter_cap: float = 100.0
    spirit_active: bool = False
    level_reached: int = 1
    inventory: list = field(default_factory=list)
    unlocked_outfits: list = field(default_factory=lambda: ["shepherd_rags"])
    unlocked_weapons: list = field(default_factory=lambda: ["sling_basic", "staff"])

    def gain_faith(self, amount: float, reason: str = "") -> float:
        prev = self.faith_meter
        self.faith_meter = min(self.faith_meter + amount, self.faith_meter_cap)
        gained = self.faith_meter - prev
        if reason:
            print(f"[Faith +{gained:.1f}] {reason}")
        return gained

    def spend_faith(self, amount: float) -> bool:
        if self.faith_meter < amount:
            print(f"[Faith] Not enough faith ({self.faith_meter:.1f}/{amount})")
            return False
        self.faith_meter -= amount
        return True

    def activate_spirit(self) -> bool:
        if not self.spend_faith(25):
            return False
        self.spirit_active = True
        self.stats.speed *= 1.4
        self.stats.strength = int(self.stats.strength * 1.6)
        print("[Spirit of the Lord] David's courage surges! Speed and strength increased.")
        return True

    def deactivate_spirit(self):
        if self.spirit_active:
            self.stats.speed /= 1.4
            self.stats.strength = int(self.stats.strength / 1.6)
            self.spirit_active = False

    def take_damage(self, amount: int) -> bool:
        effective = max(0, amount - self.stats.defense)
        self.stats.health = max(0, self.stats.health - effective)
        print(f"[Health] David takes {effective} damage. ({self.stats.health}/{self.stats.max_health})")
        return self.stats.health > 0

    def heal(self, amount: int):
        self.stats.health = min(self.stats.max_health, self.stats.health + amount)
        print(f"[Health] David heals {amount}. ({self.stats.health}/{self.stats.max_health})")

    def equip_outfit(self, outfit_id: str) -> bool:
        if outfit_id not in self.unlocked_outfits:
            print(f"[Outfit] '{outfit_id}' not yet unlocked.")
            return False
        self.equipment.outfit = outfit_id
        print(f"[Outfit] Equipped: {outfit_id}")
        return True

    def equip_weapon(self, weapon_id: str) -> bool:
        if weapon_id not in self.unlocked_weapons:
            print(f"[Weapon] '{weapon_id}' not yet unlocked.")
            return False
        self.equipment.weapon = weapon_id
        print(f"[Weapon] Equipped: {weapon_id}")
        return True

    def unlock_item(self, item_id: str):
        self.inventory.append(item_id)
        print(f"[Inventory] Received: {item_id}")

    def status(self) -> str:
        faith_bar = self._bar(self.faith_meter, self.faith_meter_cap)
        health_bar = self._bar(self.stats.health, self.stats.max_health)
        spirit_tag = " [SPIRIT ACTIVE]" if self.spirit_active else ""
        return (
            f"══ {self.name}, {self.title}{spirit_tag} ══\n"
            f"  Health : {health_bar} {self.stats.health}/{self.stats.max_health}\n"
            f"  Faith  : {faith_bar} {self.faith_meter:.0f}/{self.faith_meter_cap:.0f}\n"
            f"  Speed  : {self.stats.speed:.1f}  Strength: {self.stats.strength}  "
            f"Defense: {self.stats.defense}  Stealth: {self.stats.stealth}\n"
            f"  Weapon : {self.equipment.weapon}  Outfit: {self.equipment.outfit}"
        )

    @staticmethod
    def _bar(current: float, maximum: float, width: int = 20) -> str:
        filled = int((current / maximum) * width) if maximum > 0 else 0
        return f"[{'█' * filled}{'░' * (width - filled)}]"
