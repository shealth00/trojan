"""
Flock management mechanic. Discrete-event 1-D simulation (0-100 units).
"""

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Sheep:
    sheep_id: int
    position: float = 50.0
    safe: bool = False
    captured: bool = False

    def wander(self, water_position: float = 80.0):
        if not self.safe and not self.captured:
            drift = 2.0 if self.position < water_position else -1.0
            self.position = max(0.0, min(100.0, self.position + drift + random.uniform(-3, 3)))


@dataclass
class Predator:
    predator_id: int
    kind: str
    position: float
    speed: float
    target: Optional[int] = None

    def move_toward(self, dest: float):
        direction = 1 if dest > self.position else -1
        self.position += direction * min(self.speed, abs(dest - self.position))

    def distance_to(self, pos: float) -> float:
        return abs(self.position - pos)


@dataclass
class FlockState:
    sheep: list[Sheep] = field(default_factory=list)
    predators: list[Predator] = field(default_factory=list)
    david_position: float = 50.0
    david_speed: float = 8.0
    water_position: float = 80.0
    tick: int = 0
    events: list[str] = field(default_factory=list)


class FlockMechanic:
    CAPTURE_DISTANCE = 3.0
    DAVID_INTERVENE_DISTANCE = 5.0

    def __init__(self, flock_size: int = 12):
        self.flock_size = flock_size

    def new_state(self) -> FlockState:
        sheep = [Sheep(i, position=random.uniform(40, 75)) for i in range(self.flock_size)]
        return FlockState(sheep=sheep)

    def tick(self, state: FlockState, david_target: Optional[float] = None) -> FlockState:
        state.tick += 1
        state.events.clear()
        if david_target is None:
            david_target = self._most_endangered(state)
        if david_target is not None:
            direction = 1 if david_target > state.david_position else -1
            state.david_position += direction * min(state.david_speed,
                                                    abs(david_target - state.david_position))
        for sheep in state.sheep:
            sheep.wander(state.water_position)
            if not sheep.safe and abs(sheep.position - state.water_position) < 4.0:
                sheep.safe = True
                state.events.append(f"Sheep #{sheep.sheep_id} reached water safely.")
        for pred in state.predators:
            target_sheep = self._select_target(pred, state)
            if target_sheep is None:
                continue
            pred.target = target_sheep.sheep_id
            pred.move_toward(target_sheep.position)
            if pred.distance_to(target_sheep.position) <= self.CAPTURE_DISTANCE:
                if abs(state.david_position - target_sheep.position) <= self.DAVID_INTERVENE_DISTANCE:
                    state.events.append(f"David drives off the {pred.kind} threatening sheep #{target_sheep.sheep_id}!")
                    pred.position = 0.0
                else:
                    target_sheep.captured = True
                    state.events.append(f"A {pred.kind} captured sheep #{target_sheep.sheep_id}! David must act!")
        return state

    def spawn_predator(self, state: FlockState, kind: str = "wolf"):
        speeds = {"jackal": 7.0, "wolf": 9.0, "lion": 8.0}
        pred = Predator(predator_id=len(state.predators), kind=kind,
                        position=random.choice([0.0, 100.0]), speed=speeds.get(kind, 7.0))
        state.predators.append(pred)
        state.events.append(f"A {kind} appears at position {pred.position:.0f}!")

    def summary(self, state: FlockState) -> str:
        safe = sum(1 for s in state.sheep if s.safe)
        lost = sum(1 for s in state.sheep if s.captured)
        remaining = self.flock_size - safe - lost
        return (f"Tick {state.tick} | Flock: {self.flock_size} | "
                f"Safe: {safe} | Lost: {lost} | Wandering: {remaining} | Predators: {len(state.predators)}")

    def _most_endangered(self, state: FlockState) -> Optional[float]:
        endangered = None
        min_dist = float("inf")
        for pred in state.predators:
            for sheep in state.sheep:
                if sheep.safe or sheep.captured:
                    continue
                d = pred.distance_to(sheep.position)
                if d < min_dist:
                    min_dist = d
                    endangered = sheep.position
        return endangered

    def _select_target(self, pred: Predator, state: FlockState) -> Optional[Sheep]:
        vulnerable = [s for s in state.sheep if not s.safe and not s.captured]
        if not vulnerable:
            return None
        return min(vulnerable, key=lambda s: pred.distance_to(s.position))
