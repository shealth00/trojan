"""
Harp / Lyre rhythm mechanic.
"""

import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional


NOTES = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Ti"]
NOTE_COLORS = {"Do": "♩", "Re": "♪", "Mi": "♫", "Fa": "♬", "Sol": "♩", "La": "♪", "Ti": "♫"}


class HarpEffect(Enum):
    SOOTHE = "soothe"
    INSPIRE = "inspire"
    WORSHIP = "worship"


@dataclass
class SessionResult:
    notes_total: int
    notes_hit: int
    streak_max: int
    accuracy: float
    effect: Optional[HarpEffect]
    effect_magnitude: float
    message: str


class HarpMechanic:
    def __init__(self, string_type: str = "gut"):
        quality = {"gut": 1.0, "silver": 1.3, "gold": 1.6}
        self.quality_multiplier = quality.get(string_type, 1.0)
        self.string_type = string_type

    def play_session(
        self,
        effect: HarpEffect,
        note_count: int = 8,
        madness_level: float = 0.0,
        player_skill: float = 0.75,
        verbose: bool = True,
    ) -> SessionResult:
        sequence = self._generate_sequence(note_count, madness_level)
        hit_count = 0
        streak = 0
        max_streak = 0

        if verbose:
            print(f"\n  ♬ David lifts the {self.string_type}-string lyre...")

        for i, note in enumerate(sequence):
            window = self._time_window(madness_level)
            player_hit = self._player_input(note, window, player_skill, madness_level)
            if verbose:
                symbol = "✓" if player_hit else "✗"
                print(f"    [{i+1:2}/{note_count}]  {NOTE_COLORS.get(note, '♩')} {note:<4}  "
                      f"window={window:.2f}s  {symbol}")
                time.sleep(0.05)
            if player_hit:
                hit_count += 1
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        accuracy = hit_count / note_count
        magnitude = min(1.0, accuracy * self.quality_multiplier)
        message = self._session_message(accuracy, effect, madness_level)

        if verbose:
            print(f"\n  Result: {hit_count}/{note_count} notes  |  Best streak: {max_streak}  |  {message}")

        return SessionResult(
            notes_total=note_count, notes_hit=hit_count, streak_max=max_streak,
            accuracy=accuracy, effect=effect if accuracy > 0.4 else None,
            effect_magnitude=magnitude, message=message,
        )

    def soothe_saul(self, saul_rage: float, player_skill: float = 0.75, verbose: bool = True) -> tuple[float, bool]:
        if verbose:
            print(f"\n  [Saul's Rage: {saul_rage:.0%}]  David begins to play...")
        result = self.play_session(HarpEffect.SOOTHE, note_count=10,
                                   madness_level=saul_rage, player_skill=player_skill, verbose=verbose)
        soothed_by = result.effect_magnitude * 0.4 if result.effect else 0.05
        new_rage = max(0.0, saul_rage - soothed_by)
        javelin = new_rage > 0.7 and random.random() < 0.5
        if verbose:
            print(f"  Saul's rage: {saul_rage:.0%} → {new_rage:.0%}")
            if javelin:
                print("  !! JAVELIN THROWN — Quick-time event: DODGE!")
        return new_rage, javelin

    def _generate_sequence(self, count: int, madness: float) -> list[str]:
        pool = NOTES[:5] if madness < 0.3 else (NOTES if madness < 0.6 else NOTES * 2)
        return [random.choice(pool) for _ in range(count)]

    def _time_window(self, madness: float) -> float:
        return max(0.3, 1.2 - madness * 0.9)

    def _player_input(self, note: str, window: float, skill: float, madness: float) -> bool:
        return random.random() < skill * (1.0 - madness * 0.3)

    def _session_message(self, accuracy: float, effect: HarpEffect, madness: float) -> str:
        if accuracy >= 0.9: return f"Masterful playing — {effect.value} effect is powerful."
        if accuracy >= 0.7: return f"Good performance — moderate {effect.value}."
        if accuracy >= 0.4: return f"Rough session — weak {effect.value}."
        return "The melody falters — no effect."

    def upgrade_strings(self, new_type: str) -> "HarpMechanic":
        print(f"[Harp] Restrung from '{self.string_type}' to '{new_type}' strings")
        return HarpMechanic(new_type)
