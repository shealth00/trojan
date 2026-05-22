"""
Level 5 — Covenant of Brotherhood
"""

import random
import time
from dataclasses import dataclass

from ..mechanics.faith import FaithAction, FaithMeter
from .base import BaseLevel, LevelResult


@dataclass
class Encounter:
    name: str
    guard_count: int
    puzzle: str


ENCOUNTERS = [
    Encounter("Patrol at Gibeah gate",         3, "distract"),
    Encounter("Scouts on the Ziph road",       2, "hide"),
    Encounter("Ambush near the caves",         5, "signal"),
    Encounter("Royal guard at the waypoint",   4, "hide"),
    Encounter("Final pursuit — open ground",   6, "distract"),
]

PUZZLE_FLAVOR = {
    "distract": "Jonathan creates a diversion at the far end of the camp.",
    "hide":     "David presses against the cave wall; Jonathan signals 'all clear.'",
    "signal":   "Three arrows beyond the stone — the code that says 'go, flee!'",
}


class Level5Covenant(BaseLevel):
    level_id = 5
    name = "Covenant of Brotherhood"
    scripture = "1 Samuel 20:42  —  'The LORD is witness between you and me forever.'"

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        faith = FaithMeter(current=self.david.faith_meter, cap=self.david.faith_meter_cap)

        print("Jonathan whispers: 'Whatever you want me to do, I will do for you.'\n")
        time.sleep(0.4)

        evaded_count = 0
        detected_count = 0

        for i, enc in enumerate(ENCOUNTERS, 1):
            print(f"── Encounter {i}/{len(ENCOUNTERS)}: {enc.name} ──")
            print(f"   Guards: {enc.guard_count}   Puzzle: {enc.puzzle}")
            print(f"   {PUZZLE_FLAVOR[enc.puzzle]}")
            success = self._resolve_encounter(enc)
            if success:
                evaded_count += 1
                faith.apply(FaithAction.ACT_OF_COURAGE, f"evaded {enc.name}")
                print("   ✓ Slipped through undetected.\n")
            else:
                detected_count += 1
                dmg = random.randint(8, 18)
                self.david.take_damage(dmg)
                print(f"   ✗ Detected! David takes {dmg} damage in the skirmish.\n")
            time.sleep(0.1)

        self.david.faith_meter = faith.current

        if evaded_count >= 3:
            result.objectives_met.append(f"Evaded {evaded_count}/5 hunting parties")
            result.faith_earned += self._award_faith(15, "survived Saul's pursuit")
        else:
            result.objectives_missed.append(f"Only evaded {evaded_count}/5 parties")

        print("── Jonathan's Covenant ──\n")
        time.sleep(0.3)
        print("  Jonathan: 'Go in peace. We have sworn friendship in the name of the LORD.'")
        time.sleep(0.4)
        print("  He removes his royal robe and places it on David's shoulders.")
        time.sleep(0.3)
        print("  Then his tunic, his sword, his bow, and his belt.\n")
        time.sleep(0.5)

        covenant_items = ["jonathan_robe", "jonathan_sword", "jonathan_bow"]
        for item in covenant_items:
            self.david.unlock_item(item)
            result.items_unlocked.append(item)

        self.david.unlocked_outfits.append("jonathan_robe")
        self.david.unlocked_weapons += ["jonathan_sword", "jonathan_bow"]

        faith.apply(FaithAction.SPARE_ENEMY, "honored the covenant")
        self.david.faith_meter = faith.current
        result.faith_earned += 15.0
        result.objectives_met.append("Covenant with Jonathan sealed")
        result.completed = evaded_count >= 3
        result.next_level = 6 if result.completed else None

        print(result.summary())
        return result

    def _resolve_encounter(self, enc: Encounter) -> bool:
        base_success = {"distract": 0.78, "hide": 0.82, "signal": 0.70}
        difficulty_penalty = (enc.guard_count - 2) * 0.04
        chance = max(0.3, base_success.get(enc.puzzle, 0.7) - difficulty_penalty)
        return random.random() < chance
