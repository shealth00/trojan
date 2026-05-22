"""
Level 1 — The Shepherd's Duty
"""

import time

from ..entities.david import David
from ..entities.enemies import spawn
from ..mechanics.flock import FlockMechanic
from ..mechanics.sling import SlingMechanic
from .base import BaseLevel, LevelResult


class Level1ShepherdsDuty(BaseLevel):
    level_id = 1
    name = "The Shepherd's Duty"
    scripture = "1 Samuel 16:11  —  'He is tending the sheep.'"

    def run(self) -> LevelResult:
        self.intro()
        result = LevelResult(level_id=self.level_id, completed=False)
        flock = FlockMechanic(flock_size=12)
        sling = SlingMechanic("basic")
        state = flock.new_state()

        print("Phase 1 — Guide the flock to the brook while wolves circle...\n")
        for wave in range(1, 4):
            kind = "wolf" if wave % 2 == 0 else "jackal"
            flock.spawn_predator(state, kind)
            print(f"  Wave {wave}: a {kind} appears!")
            for _ in range(6):
                state = flock.tick(state)
                for event in state.events:
                    print(f"  {event}")
            print(f"  {flock.summary(state)}\n")
            time.sleep(0.1)

        sheep_safe = sum(1 for s in state.sheep if s.safe)
        sheep_lost = sum(1 for s in state.sheep if s.captured)

        if sheep_safe >= 10:
            result.objectives_met.append(f"Guided flock to water ({sheep_safe}/12 safe)")
            result.faith_earned += self._award_faith(15, "protected the flock")
        else:
            result.objectives_missed.append(f"Too many sheep lost ({sheep_lost} captured)")

        print(f"  {sheep_safe} sheep reached the brook safely. {sheep_lost} were lost.\n")

        print("Phase 2a — Boss: A lion seizes a lamb!\n")
        lion = spawn("lion")
        rounds = 0
        while lion.alive and rounds < 8:
            rounds += 1
            result_shot = sling.shoot(lion, player_skill=0.65, verbose=True)
            if result_shot.hit and lion.alive:
                dmg = lion.attack()
                self.david.take_damage(dmg)
            if not self.david.stats.health > 0:
                print("  David falls...")
                return result
            time.sleep(0.05)

        if not lion.alive:
            result.objectives_met.append("Defeated the lion")
            result.faith_earned += self._award_faith(10, "killed the lion")
            print(f"\n  The lion flees! David recovers the lamb.\n")
        else:
            result.objectives_missed.append("Lion not defeated in time")

        print("Phase 2b — Boss: A bear charges!\n")
        bear = spawn("bear")
        rounds = 0
        while bear.alive and rounds < 10:
            rounds += 1
            result_shot = sling.shoot(bear, player_skill=0.65, verbose=True)
            if result_shot.hit and bear.alive:
                dmg = bear.attack()
                self.david.take_damage(dmg)
            if not self.david.stats.health > 0:
                print("  David is overcome...")
                return result
            time.sleep(0.05)

        if not bear.alive:
            result.objectives_met.append("Defeated the bear")
            result.faith_earned += self._award_faith(15, "killed the bear")
            print(f"\n  The bear collapses. The flock is safe!\n")

        all_bosses_dead = not lion.alive and not bear.alive
        result.completed = sheep_safe >= 10 and all_bosses_dead

        if result.completed:
            self.david.unlock_item("sling_upgrade_basic")
            result.items_unlocked.append("sling_upgrade_basic")
            self.david.gain_faith(5, "level complete bonus")
            result.faith_earned += 5
            print("\n  In the distance, a procession approaches Bethlehem—\n  the prophet Samuel has come.\n")

        print(result.summary())
        return result
