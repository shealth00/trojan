"""
The Shepherd King — game session orchestrator.

Initialises David, runs levels in sequence, and carries state between them.
"""

import time
from typing import Optional

from .entities.david import David
from .levels.base import LevelResult
from .levels.level1_shepherd import Level1ShepherdsDuty
from .levels.level2_anointing import Level2Anointing
from .levels.level3_melancholy import Level3KingsMelancholy
from .levels.level4_valley_of_elah import Level4ValleyOfElah
from .levels.level5_covenant import Level5Covenant
from .levels.level6_jebus import Level6Jebus
from .levels.level7_crown import Level7Crown

LEVEL_MAP = {
    1: Level1ShepherdsDuty,
    2: Level2Anointing,
    3: Level3KingsMelancholy,
    4: Level4ValleyOfElah,
    5: Level5Covenant,
    6: Level6Jebus,
    7: Level7Crown,
}


class Game:
    def __init__(self, start_level: int = 1, player_skill: float = 0.75):
        self.david = David()
        self.current_level = start_level
        self.player_skill = player_skill
        self.completed_levels: list[int] = []
        self.total_faith_earned: float = 0.0

    MAX_RETRIES = 3

    def run(self, max_levels: Optional[int] = None) -> None:
        self._title_screen()
        level_num = self.current_level

        while level_num in LEVEL_MAP:
            if max_levels and len(self.completed_levels) >= max_levels:
                break

            level_class = LEVEL_MAP[level_num]
            completed = False

            for attempt in range(1, self.MAX_RETRIES + 1):
                self.david.heal(self.david.stats.max_health)  # full heal each attempt
                level = level_class(self.david)
                result = level.run()
                self.total_faith_earned += result.faith_earned

                if result.completed:
                    completed = True
                    break
                print(f"\n  Level {level_num} not completed (attempt {attempt}/{self.MAX_RETRIES}). Retrying...\n")

            self._rest_between_levels()

            if completed:
                self.completed_levels.append(level_num)
                level_num = result.next_level or (level_num + 1)
                if level_num > 7:
                    break
            else:
                print(f"\n  Could not complete level {level_num} after {self.MAX_RETRIES} attempts. Moving on.\n")
                level_num += 1

        self._end_screen()

    def _rest_between_levels(self):
        print("\n  ── Rest ──")
        heal_amount = 40
        self.david.heal(heal_amount)
        time.sleep(0.2)
        print(f"  David rests. ({self.david.stats.health}/{self.david.stats.max_health} HP)\n")
        print(self.david.status())
        print()
        time.sleep(0.3)

    def _title_screen(self):
        print(
            "\n"
            "  ╔══════════════════════════════════════════╗\n"
            "  ║         T H E   S H E P H E R D         ║\n"
            "  ║                   K I N G                ║\n"
            "  ╚══════════════════════════════════════════╝\n"
            "\n"
            "  'I have found David son of Jesse, a man after my own heart.'\n"
            "                                          — Acts 13:22\n"
        )
        time.sleep(0.5)

    def _end_screen(self):
        levels_done = len(self.completed_levels)
        print(
            f"\n  ══ Session Complete ══\n"
            f"  Levels completed : {levels_done}/7\n"
            f"  Total faith earned: {self.total_faith_earned:.1f}\n"
            f"  Final title       : {self.david.title}\n"
        )
        print(self.david.status())
