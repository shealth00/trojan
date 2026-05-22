"""
Level 2 — The Anointing
"""

import time

from ..entities.david import David
from ..mechanics.faith import FaithMeter, FaithAction
from .base import BaseLevel, LevelResult

CHORES = [
    ("Draw water from the well",       FaithAction.OBEY_COMMAND, 6.0),
    ("Stack grain in the storehouse",  FaithAction.OBEY_COMMAND, 6.0),
    ("Repair the sheep pen fence",     FaithAction.ACT_OF_COURAGE, 4.0),
    ("Prepare food for Samuel's visit",FaithAction.OBEY_COMMAND, 5.0),
]


class Level2Anointing(BaseLevel):
    level_id = 2
    name = "The Anointing"
    scripture = "1 Samuel 16:12-13  —  'Rise and anoint him; this is the one.'"

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        faith = FaithMeter(current=self.david.faith_meter, cap=self.david.faith_meter_cap)

        print("Phase 1 — Complete chores before Samuel arrives...\n")
        completed_chores = 0
        for description, action, bonus in CHORES:
            print(f"  Chore: {description}")
            faith.apply(action, description)
            self.david.faith_meter = faith.current
            completed_chores += 1
            time.sleep(0.1)

        if completed_chores == len(CHORES):
            result.objectives_met.append("All chores completed")
            result.faith_earned += 21.0

        print("\nPhase 2 — Samuel reviews Jesse's sons...\n")
        brothers = ["Eliab", "Abinadab", "Shammah", "Nethanel", "Raddai", "Ozem", "Elihu"]
        for name in brothers:
            print(f"  Samuel looks upon {name}...")
            time.sleep(0.08)
            print(f"  'The Lord has not chosen {name}.'\n")

        print("  Samuel: 'Are these all your sons, Jesse?'")
        time.sleep(0.2)
        print("  Jesse: 'The youngest remains — he tends the sheep.'")
        time.sleep(0.2)
        print("  Samuel: 'Send for him. We will not sit until he arrives.'\n")
        time.sleep(0.3)
        result.objectives_met.append("Witnessed Samuel's review of the brothers")

        print("Phase 3 — David is called from the field...\n")
        time.sleep(0.4)
        print("  David stands before Samuel, ruddy-cheeked and bright-eyed.\n")
        time.sleep(0.3)
        print("  The LORD says to Samuel: 'Rise and anoint him; this is the one.'\n")
        time.sleep(0.4)
        print("  ══ Samuel pours the anointing oil over David's head. ══")
        time.sleep(0.5)
        print("  From this day forward, the Spirit of the LORD rests upon David.\n")

        faith.apply(FaithAction.PRAYER, "anointing by Samuel")
        faith.expand_cap(25.0, "Spirit of the Lord unlocked")
        self.david.faith_meter = faith.current
        self.david.faith_meter_cap = faith.cap

        result.objectives_met.append("Received the anointing")
        result.items_unlocked += ["spirit_of_the_lord_meter", "harp_unlock"]
        result.faith_earned += faith.current
        result.completed = True
        result.next_level = 3

        self.david.unlock_item("harp_gut")
        print(result.summary())
        return result
