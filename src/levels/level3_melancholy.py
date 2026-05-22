"""
Level 3 — The King's Melancholy
"""

import random
import time

from ..mechanics.harp import HarpMechanic, HarpEffect
from .base import BaseLevel, LevelResult


class Level3KingsMelancholy(BaseLevel):
    level_id = 3
    name = "The King's Melancholy"
    scripture = "1 Samuel 16:23  —  'Saul would be relieved and feel better.'"
    SESSIONS = 5
    INITIAL_RAGE = 0.3

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        harp = HarpMechanic(string_type="gut")
        saul_rage = self.INITIAL_RAGE
        javelins_thrown = 0
        javelins_survived = 0
        sessions_calmed = 0

        print(f"David enters the torch-lit halls of Saul's palace...\n")
        time.sleep(0.3)

        for session in range(1, self.SESSIONS + 1):
            print(f"\n── Session {session}/{self.SESSIONS} ──  Saul's rage: {saul_rage:.0%}")
            new_rage, javelin = harp.soothe_saul(saul_rage=saul_rage, player_skill=0.75, verbose=True)

            if new_rage < saul_rage:
                sessions_calmed += 1

            if javelin:
                javelins_thrown += 1
                survived = self._dodge_qte()
                if survived:
                    javelins_survived += 1
                    print("  David sidesteps — the javelin clatters against the wall.")
                    self.david.gain_faith(3, "dodged Saul's javelin")
                    result.faith_earned += 3
                else:
                    dmg = random.randint(20, 35)
                    alive = self.david.take_damage(dmg)
                    print(f"  The javelin grazes David — {dmg} damage!")
                    if not alive:
                        print("  David collapses in the palace hall...")
                        result.objectives_missed.append("Fell to Saul's javelin")
                        print(result.summary())
                        return result

            saul_rage = min(1.0, new_rage + 0.08)
            time.sleep(0.1)

        if sessions_calmed >= 3:
            result.objectives_met.append(f"Calmed Saul in {sessions_calmed}/5 sessions")
            result.faith_earned += self._award_faith(12, "faithfully played for the king")
        else:
            result.objectives_missed.append(f"Only calmed Saul {sessions_calmed}/5 sessions")

        if javelins_thrown == 0:
            result.objectives_met.append("Kept Saul calm — no javelins thrown")
        elif javelins_survived >= javelins_thrown:
            result.objectives_met.append(f"Survived all {javelins_thrown} javelin throws")
        else:
            result.objectives_missed.append(f"Hit by {javelins_thrown - javelins_survived} javelin(s)")

        if saul_rage < 0.2:
            result.objectives_met.append("Saul fully soothed — bonus achieved")
            result.items_unlocked.append("harp_mastery_strings")
            result.faith_earned += self._award_faith(8, "perfect calm maintained")

        result.completed = sessions_calmed >= 3
        result.next_level = 4 if result.completed else None

        if result.completed:
            self.david.unlock_item("harp_silver_strings")
            result.items_unlocked.append("royal_favor")
            print("\n  Saul says: 'Play for me again tomorrow, boy.'\n  Word of David's courage and music spreads through the palace.\n")

        print(result.summary())
        return result

    def _dodge_qte(self, skill: float = 0.75) -> bool:
        print("  !! DODGE QTE — Press [SPACE] at the right moment!")
        time.sleep(0.1)
        return random.random() < skill
