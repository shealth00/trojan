"""
Faith / Spirit Meter system.
"""

from dataclasses import dataclass, field
from enum import Enum


class FaithAction(Enum):
    PRAYER = ("prayer", 10.0)
    WORSHIP_MUSIC = ("worship_music", 8.0)
    ACT_OF_COURAGE = ("act_of_courage", 5.0)
    SPARE_ENEMY = ("spare_enemy", 15.0)
    OBEY_COMMAND = ("obey_command", 7.0)
    IDLE = ("idle", -1.0)
    DOUBT = ("doubt", -5.0)
    DISOBEY = ("disobey", -12.0)

    def __init__(self, action_id: str, delta: float):
        self.action_id = action_id
        self.delta = delta


@dataclass
class FaithEvent:
    action: FaithAction
    context: str = ""
    delta_applied: float = 0.0


@dataclass
class FaithMeter:
    current: float = 0.0
    cap: float = 100.0
    history: list[FaithEvent] = field(default_factory=list)

    def apply(self, action: FaithAction, context: str = "", verbose: bool = True) -> float:
        delta = action.delta
        before = self.current
        self.current = max(0.0, min(self.cap, self.current + delta))
        actual_delta = self.current - before
        event = FaithEvent(action, context, actual_delta)
        self.history.append(event)
        if verbose:
            sign = "+" if actual_delta >= 0 else ""
            ctx = f" ({context})" if context else ""
            print(f"  [Faith] {action.action_id}{ctx}  {sign}{actual_delta:.1f}  →  {self.current:.1f}/{self.cap:.1f}")
        return actual_delta

    def expand_cap(self, amount: float, reason: str = ""):
        self.cap = min(200.0, self.cap + amount)
        tag = f" ({reason})" if reason else ""
        print(f"  [Faith] Capacity expanded{tag}: cap is now {self.cap:.0f}")

    def is_full(self) -> bool:
        return self.current >= self.cap

    def percentage(self) -> float:
        return self.current / self.cap if self.cap > 0 else 0.0

    def drain(self, amount: float) -> float:
        prev = self.current
        self.current = max(0.0, self.current - amount)
        return prev - self.current

    def can_activate_spirit(self, cost: float = 25.0) -> bool:
        return self.current >= cost

    def bar(self, width: int = 24) -> str:
        filled = int(self.percentage() * width)
        return f"[{'█' * filled}{'░' * (width - filled)}] {self.current:.0f}/{self.cap:.0f}"

    def recent_history(self, n: int = 5) -> str:
        lines = []
        for e in self.history[-n:]:
            sign = "+" if e.delta_applied >= 0 else ""
            lines.append(f"  {e.action.action_id:<20} {sign}{e.delta_applied:.1f}")
        return "\n".join(lines) if lines else "  (no events yet)"
