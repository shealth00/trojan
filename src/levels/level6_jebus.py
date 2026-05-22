"""
Level 6 — The Stronghold of Jebus
"""

import random
import time

from ..entities.enemies import spawn
from ..mechanics.sling import SlingMechanic
from ..mechanics.faith import FaithAction, FaithMeter
from .base import BaseLevel, LevelResult

JEBUSITE_TAUNT = (
    "'Even the blind and the lame can ward you off!' — the Jebusites call out.\n"
    "  'David will never get in here.'"
)


class Level6Jebus(BaseLevel):
    level_id = 6
    name = "The Stronghold of Jebus"
    scripture = "2 Samuel 5:7  —  'David captured the fortress of Zion.'"

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        faith = FaithMeter(current=self.david.faith_meter, cap=self.david.faith_meter_cap)

        print(JEBUSITE_TAUNT)
        time.sleep(0.5)
        print("\nDavid surveys the walls... then notices the gully below.\n")
        time.sleep(0.4)
        print("  'Whoever would strike the Jebusites, let him reach them by the water shaft.'\n")
        time.sleep(0.3)

        result.objectives_met.append("Discovered the water shaft")
        faith.apply(FaithAction.ACT_OF_COURAGE, "devised the shaft plan")

        print("── Segment 1: The Climb ──\n")
        if not self._traverse_segment("Gripping wet stone, David's men scale the dark shaft...",
                                      difficulty=0.30, hazard="falling", hazard_dmg=(10, 20)):
            result.objectives_missed.append("Failed the climb — fell in the shaft")
            print(result.summary())
            return result
        result.objectives_met.append("Scaled the water shaft")
        result.faith_earned += self._award_faith(8, "climbed the shaft")
        faith.apply(FaithAction.ACT_OF_COURAGE, "climbed the shaft")

        print("\n── Segment 2: The Swim ──\n")
        if not self._traverse_segment("Cold rushing water. The men swim against the current...",
                                      difficulty=0.25, hazard="drowning", hazard_dmg=(15, 25)):
            result.objectives_missed.append("Overwhelmed by the current")
            print(result.summary())
            return result
        result.objectives_met.append("Swam the inner reservoir")
        result.faith_earned += self._award_faith(8, "swam through the shaft")

        print("\n── Segment 3: Inner Guards ──\n")
        guards = [spawn("jebusite_guard") for _ in range(3)]
        sling = SlingMechanic("braided" if "sling_braided" in self.david.inventory else "basic")
        for guard in guards:
            print(f"  {guard.name} blocks the path!")
            self._fight_enemy(guard, sling)
            if self.david.stats.health <= 0:
                result.objectives_missed.append("Fell to inner guards")
                print(result.summary())
                return result
        result.objectives_met.append("Cleared the inner guards")

        print("\n  David reaches the city gates and heaves the bar aside...")
        time.sleep(0.4)
        print("  Israel's army pours in. The city of Jebus is breached!\n")
        time.sleep(0.3)

        print("── Boss: Jebusite King ──\n")
        king = spawn("jebusite_king")
        print(f"  The Jebusite King stands in the gatehouse — {king.health} HP\n")

        rounds = 0
        while king.alive and rounds < 15:
            rounds += 1
            exposed = rounds % 4 == 0
            shot = sling.shoot(king, player_skill=0.78, target_exposed=exposed, verbose=True)
            if king.alive:
                dmg = king.attack()
                alive = self.david.take_damage(dmg)
                if not alive:
                    result.objectives_missed.append("Defeated by the Jebusite king")
                    print(result.summary())
                    return result
            time.sleep(0.05)

        if not king.alive:
            print("\n  The Jebusite king falls. Jerusalem belongs to Israel!\n")
            result.objectives_met.append("Defeated the Jebusite king")
            result.faith_earned += self._award_faith(20, "captured Jerusalem")
            faith.expand_cap(10.0, "City of David established")
            self.david.faith_meter_cap = faith.cap
            result.items_unlocked += ["city_of_david_unlocked", "jerusalem_throne"]
            result.completed = True
            result.next_level = 7

        print(result.summary())
        return result

    def _traverse_segment(self, flavor, difficulty, hazard, hazard_dmg):
        print(f"  {flavor}")
        time.sleep(0.3)
        if random.random() < difficulty:
            lo, hi = hazard_dmg
            dmg = random.randint(lo, hi)
            print(f"  Hazard ({hazard})! David takes {dmg} damage.")
            return self.david.take_damage(dmg)
        print("  Passed safely.\n")
        return True

    def _fight_enemy(self, enemy, sling):
        while enemy.alive and self.david.stats.health > 0:
            sling.shoot(enemy, player_skill=0.75, verbose=True)
            if enemy.alive:
                self.david.take_damage(enemy.attack())
        if not enemy.alive:
            print(f"  {enemy.name} defeated.\n")
