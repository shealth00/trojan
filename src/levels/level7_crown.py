"""
Level 7 — The Crown of Israel
"""

import random
import time
from dataclasses import dataclass

from ..mechanics.harp import HarpMechanic, HarpEffect
from ..mechanics.faith import FaithAction, FaithMeter
from .base import BaseLevel, LevelResult


@dataclass
class BattleFront:
    name: str
    enemy_force: str
    troop_strength: int
    difficulty: float


FRONTS = [
    BattleFront("Philistine advance at Rephaim",      "philistine_army",  85, 0.35),
    BattleFront("Moabite incursion at the Dead Sea",  "moabite_force",    90, 0.30),
    BattleFront("Ammonite raid on the eastern border","ammonite_raider",  75, 0.40),
]

ARK_PROCESSION_NOTES = 12


class Level7Crown(BaseLevel):
    level_id = 7
    name = "The Crown of Israel"
    scripture = "2 Samuel 6:14  —  'David danced before the LORD with all his might.'"

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        faith = FaithMeter(current=self.david.faith_meter, cap=self.david.faith_meter_cap)

        print("The kingdom of Israel must be secured before the Ark returns...\n")
        victories = 0
        for front in FRONTS:
            print(f"── Battle Front: {front.name} ──")
            print(f"   Enemy: {front.enemy_force.replace('_', ' ').title()}")
            print(f"   Troop strength: {front.troop_strength}%")
            if self._resolve_battle(front):
                victories += 1
                faith.apply(FaithAction.ACT_OF_COURAGE, f"won battle at {front.name}")
                result.faith_earned += self._award_faith(10, f"victory at {front.name}")
                print(f"   ✓ Victory! The enemy is driven back.\n")
            else:
                print(f"   ✗ The line buckles — a tactical retreat.\n")
            time.sleep(0.1)

        self.david.faith_meter = faith.current

        if victories >= 2:
            result.objectives_met.append(f"Won {victories}/3 strategic battles")
        else:
            result.objectives_missed.append(f"Only won {victories}/3 battles")

        print("── The Ark of the Covenant returns to Jerusalem ──\n")
        time.sleep(0.4)
        print("  Thirty thousand chosen men of Israel accompany the Ark.")
        print("  David wears a linen ephod and leads the procession.\n")
        time.sleep(0.3)

        print("── GRAND FINALE: Dancing Before the Ark ──\n")
        print("  The city erupts. David dances with all his might before the LORD.\n")
        time.sleep(0.3)

        harp = HarpMechanic(string_type="gold")
        finale = harp.play_session(HarpEffect.WORSHIP, note_count=ARK_PROCESSION_NOTES,
                                   madness_level=0.0, player_skill=0.88, verbose=True)

        self.david.faith_meter = min(self.david.faith_meter_cap,
                                     self.david.faith_meter + finale.effect_magnitude * 40)
        result.faith_earned += finale.effect_magnitude * 40

        if finale.accuracy >= 0.8:
            result.objectives_met.append("Grand Finale: Ark enters with full celebration")
            result.items_unlocked += ["full_royal_armor", "king_of_israel_title", "ark_blessing"]
            self.david.unlock_item("full_royal_armor")
            self.david.unlocked_outfits.append("royal_armor")
        else:
            result.objectives_met.append("Ark entered Jerusalem")

        print("\n  From a palace window, Michal watches with contempt:")
        print("  'How the king of Israel has distinguished himself today...'\n")
        print("  David: 'It was before the LORD, who chose me.'")
        faith.apply(FaithAction.PRAYER, "worshipped before the Ark")
        self.david.faith_meter = faith.current
        result.faith_earned += 5
        result.objectives_met.append("Ark of the Covenant brought to Jerusalem")
        result.completed = victories >= 2 and finale.accuracy >= 0.5
        result.next_level = None

        if result.completed:
            print(
                "\n  ══════════════════════════════════════════════\n"
                "   THE SHEPHERD KING\n"
                "   From the hills of Bethlehem to the throne of Israel —\n"
                "   the story of a man after God's own heart.\n"
                "  ══════════════════════════════════════════════\n"
            )

        print(result.summary())
        return result

    def _resolve_battle(self, front: BattleFront) -> bool:
        faith_bonus = (self.david.faith_meter / self.david.faith_meter_cap) * 0.15
        win_chance = (front.troop_strength / 100.0) * (1.0 - front.difficulty) + faith_bonus
        return random.random() < win_chance
