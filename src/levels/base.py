from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from ..entities.david import David


@dataclass
class LevelResult:
    level_id: int
    completed: bool
    objectives_met: list[str] = field(default_factory=list)
    objectives_missed: list[str] = field(default_factory=list)
    faith_earned: float = 0.0
    items_unlocked: list[str] = field(default_factory=list)
    next_level: Optional[int] = None

    def summary(self) -> str:
        status = "COMPLETE" if self.completed else "FAILED"
        lines = [
            f"══ Level {self.level_id} — {status} ══",
            f"  Faith earned : {self.faith_earned:.1f}",
        ]
        for obj in self.objectives_met:
            lines.append(f"  ✓ {obj}")
        for obj in self.objectives_missed:
            lines.append(f"  ✗ {obj}")
        if self.items_unlocked:
            lines.append(f"  Unlocked: {', '.join(self.items_unlocked)}")
        return "\n".join(lines)


class BaseLevel(ABC):
    level_id: int
    name: str
    scripture: str

    def __init__(self, david: David):
        self.david = david

    def intro(self):
        print(f"\n{'═' * 60}")
        print(f"  LEVEL {self.level_id}: {self.name.upper()}")
        print(f"  {self.scripture}")
        print(f"{'═' * 60}\n")

    @abstractmethod
    def run(self) -> LevelResult:
        ...

    def _award_faith(self, amount: float, reason: str = ""):
        self.david.gain_faith(amount, reason)
        return amount
