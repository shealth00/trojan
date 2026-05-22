"""
Level 4 — The Valley of Elah
"""

import random
import time

from ..entities.enemies import spawn
from ..mechanics.sling import SlingMechanic
from ..mechanics.faith import FaithAction, FaithMeter
from .base import BaseLevel, LevelResult

GOLIATH_TAUNTS = [
    "Am I a dog, that you come at me with sticks?",
    "Come here, and I'll give your flesh to the birds!",
    "Is there no man in Israel who will face me?",
]

DAVID_REPLY = (
    "You come against me with sword and spear and javelin,\n"
    "  but I come against you in the name of the LORD Almighty,\n"
    "  the God of the armies of Israel!\n"
    "  This day the LORD will deliver you into my hands!"
)


class Level4ValleyOfElah(BaseLevel):
    level_id = 4
    name = "The Valley of Elah"
    scripture = "1 Samuel 17  —  'The battle is the LORD's.'"

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        faith = FaithMeter(current=self.david.faith_meter, cap=self.david.faith_meter_cap)

        print("Phase 1 — David refuses Saul's heavy armor.\n")
        time.sleep(0.2)
        print("  Saul's armor is tested... it slows David to a crawl.")
        print("  David removes it: 'I cannot go in these — I am not used to them.'")
        time.sleep(0.3)
        print("  He takes his staff, his sling, and walks to the brook.\n")
        faith.apply(FaithAction.ACT_OF_COURAGE, "refused Saul's armor")
        self.david.faith_meter = faith.current

        stones_needed = 5
        stones_collected = 0
        archers = [spawn("philistine_archer") for _ in range(4)]

        print("Phase 1b — Crossing the valley under fire...\n")
        for stone in range(1, stones_needed + 1):
            print(f"  Stone {stone}/5 — David dashes toward the brook!")
            for archer in archers:
                if not archer.alive:
                    continue
                if random.random() < 0.18:
                    dmg = max(1, archer.attack() // 2)
                    alive = self.david.take_damage(dmg)
                    if not alive:
                        print("  David is struck down before reaching Goliath...")
                        result.objectives_missed.append("Fell to archer fire")
                        print(result.summary())
                        return result
            stones_collected += 1
            print(f"  Stone {stone} recovered from the brook.\n")
            time.sleep(0.08)

        result.objectives_met.append(f"Collected {stones_collected}/5 smooth stones")
        result.faith_earned += self._award_faith(10, "reached the brook")

        print("\nPhase 2 — The Valley falls silent as Goliath steps forward.\n")
        time.sleep(0.4)
        print(f"  Goliath ({GOLIATH_TAUNTS[0]})")
        time.sleep(0.3)
        print(f"\n  David calls back:\n  {DAVID_REPLY}\n")
        time.sleep(0.5)
        faith.apply(FaithAction.ACT_OF_COURAGE, "challenged Goliath in faith")
        faith.apply(FaithAction.PRAYER, "called on the Lord's name")
        self.david.faith_meter = faith.current

        goliath = spawn("goliath")
        goliath.health = 30
        sling = SlingMechanic("basic")
        patterns = ["sweep_left", "sweep_right", "overhead_slam", "taunt_expose"]

        print(f"  Goliath towers over the valley. David grips the sling.\n")
        stones_used = 0
        rounds = 0
        goliath_defeated = False

        while goliath.alive and stones_used < stones_collected and rounds < 16:
            rounds += 1
            pattern = patterns[(rounds - 1) % len(patterns)]
            exposed = pattern == "taunt_expose"
            print(f"  Round {rounds}: Goliath — {pattern.replace('_', ' ').upper()}")

            if exposed:
                print(f"  Goliath taunts, forehead exposed! — '{GOLIATH_TAUNTS[rounds % len(GOLIATH_TAUNTS)]}'")
                print("  NOW — load the stone and aim for the forehead!\n")
                shot = sling.goliath_shot(goliath, player_skill=0.82)
                stones_used += 1
                result.faith_earned += self._award_faith(5, "fired at Goliath's weak point")
            else:
                alive = self._dodge_attack(pattern)
                if not alive:
                    print("  David is overcome by the giant's blow...")
                    result.objectives_missed.append("Defeated by Goliath")
                    print(result.summary())
                    return result
                continue

            if not goliath.alive:
                goliath_defeated = True
                break
            time.sleep(0.1)

        if goliath_defeated:
            print("\n  ══ GOLIATH FALLS ══")
            time.sleep(0.4)
            print("  The giant crashes to the earth. The valley trembles.")
            time.sleep(0.3)
            print("  David takes Goliath's own sword and stands over him.")
            time.sleep(0.4)
            print("\n  A roar erupts from Israel's ranks — the Philistines break and flee!\n")
            faith.apply(FaithAction.ACT_OF_COURAGE, "slew Goliath")
            self.david.faith_meter = faith.current
            faith.expand_cap(15.0, "champion of Israel")
            self.david.faith_meter_cap = faith.cap
            result.objectives_met.append("Defeated Goliath")
            result.items_unlocked += ["goliath_sword", "champion_of_israel_title", "faith_bar_expansion"]
            result.faith_earned += 25.0
            result.completed = True
            result.next_level = 5
            self.david.unlock_item("goliath_sword")
            self.david.unlocked_weapons.append("goliath_sword")
        else:
            result.objectives_missed.append("Goliath not defeated")

        print(result.summary())
        return result

    def _dodge_attack(self, pattern: str, skill: float = 0.72) -> bool:
        dodge_chance = {"sweep_left": 0.82, "sweep_right": 0.82, "overhead_slam": 0.70}
        chance = dodge_chance.get(pattern, skill)
        success = random.random() < chance
        if not success:
            import random as _r
            reduced = _r.randint(18, 32)
            alive = self.david.take_damage(reduced)
            print(f"  David is clipped by the blow! ({reduced} damage)")
            return alive
        return True
