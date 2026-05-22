import pytest
from src.entities.david import David, Stats, Equipment
from src.entities.enemies import spawn
from src.mechanics.sling import SlingMechanic
from src.mechanics.harp import HarpMechanic, HarpEffect
from src.mechanics.flock import FlockMechanic
from src.mechanics.faith import FaithMeter, FaithAction


class TestDavid:
    def test_default_stats(self):
        d = David()
        assert d.stats.health == 100
        assert d.faith_meter == 0.0
        assert "sling_basic" in d.unlocked_weapons

    def test_gain_faith_capped(self):
        d = David()
        d.faith_meter_cap = 50.0
        d.gain_faith(200)
        assert d.faith_meter == 50.0

    def test_take_damage_alive(self):
        d = David()
        alive = d.take_damage(30)
        assert alive
        assert d.stats.health == 70

    def test_take_damage_death(self):
        d = David()
        alive = d.take_damage(100)
        assert not alive
        assert d.stats.health == 0

    def test_activate_spirit_requires_faith(self):
        d = David()
        d.faith_meter = 20.0
        assert not d.activate_spirit()

    def test_activate_spirit_boosts_stats(self):
        d = David()
        d.faith_meter = 50.0
        base_speed = d.stats.speed
        d.activate_spirit()
        assert d.stats.speed > base_speed

    def test_equip_unlocked_outfit(self):
        d = David()
        d.unlocked_outfits.append("royal_armor")
        assert d.equip_outfit("royal_armor")
        assert d.equipment.outfit == "royal_armor"

    def test_equip_locked_outfit_fails(self):
        d = David()
        assert not d.equip_outfit("royal_armor")

    def test_heal_capped_at_max(self):
        d = David()
        d.take_damage(20)
        d.heal(9999)
        assert d.stats.health == d.stats.max_health


class TestEnemies:
    def test_spawn_goliath(self):
        g = spawn("goliath")
        assert g.name == "Goliath of Gath"
        assert g.health == 500
        assert g.weak_point == "forehead"
        assert g.is_boss

    def test_take_damage_weak_point_triples(self):
        g = spawn("goliath")
        hp_before = g.health
        dealt = g.take_damage(10, hit_weak_point=True)
        assert dealt == 30
        assert g.health == hp_before - 30

    def test_armor_halves_normal_damage(self):
        g = spawn("goliath")
        hp_before = g.health
        dealt = g.take_damage(20, hit_weak_point=False)
        assert dealt == 10

    def test_spawn_unknown_raises(self):
        with pytest.raises(ValueError):
            spawn("dragon_of_babel")

    def test_enemy_alive_property(self):
        wolf = spawn("wolf")
        assert wolf.alive
        wolf.take_damage(9999)
        assert not wolf.alive


class TestSling:
    def test_no_stones_no_shot(self):
        sling = SlingMechanic()
        enemy = spawn("wolf")
        result = sling.shoot(enemy, stones_remaining=0, verbose=False)
        assert not result.hit

    def test_upgrade_returns_new_instance(self):
        sling = SlingMechanic("basic")
        upgraded = sling.upgrade("braided")
        assert upgraded.sling_tier == "braided"
        assert sling.sling_tier == "basic"

    def test_perfect_shot_on_exposed_weak_point(self):
        import random
        random.seed(42)
        sling = SlingMechanic("anointed")
        enemy = spawn("goliath")
        results = [
            sling.shoot(enemy, player_skill=1.0, target_exposed=True,
                        stones_remaining=5, verbose=False)
            for _ in range(20)
        ]
        hit_count = sum(1 for r in results if r.hit)
        assert hit_count >= 15

    def test_damage_scales_with_accuracy_power(self):
        sling = SlingMechanic("basic")
        enemy = spawn("wolf")
        result = sling.shoot(enemy, player_skill=0.5, verbose=False)
        if result.hit:
            assert result.damage > 0


class TestHarp:
    def test_high_skill_mostly_hits(self):
        import random
        random.seed(0)
        harp = HarpMechanic("gold")
        result = harp.play_session(HarpEffect.SOOTHE, note_count=20,
                                   madness_level=0.0, player_skill=0.95, verbose=False)
        assert result.accuracy >= 0.7

    def test_low_skill_low_accuracy(self):
        import random
        random.seed(7)
        harp = HarpMechanic("gut")
        result = harp.play_session(HarpEffect.SOOTHE, note_count=20,
                                   madness_level=0.0, player_skill=0.1, verbose=False)
        assert result.accuracy < 0.5

    def test_effect_none_on_catastrophic_failure(self):
        import random
        random.seed(99)
        harp = HarpMechanic("gut")
        result = harp.play_session(HarpEffect.SOOTHE, note_count=20,
                                   madness_level=1.0, player_skill=0.0, verbose=False)
        assert result.effect is None or result.accuracy < 0.5

    def test_upgrade_strings(self):
        harp = HarpMechanic("gut")
        upgraded = harp.upgrade_strings("gold")
        assert upgraded.string_type == "gold"
        assert upgraded.quality_multiplier > harp.quality_multiplier

    def test_soothe_saul_reduces_rage(self):
        import random
        random.seed(1)
        harp = HarpMechanic("silver")
        new_rage, _ = harp.soothe_saul(saul_rage=0.5, player_skill=0.9, verbose=False)
        assert new_rage < 0.5


class TestFlock:
    def test_initial_flock_size(self):
        flock = FlockMechanic(flock_size=12)
        state = flock.new_state()
        assert len(state.sheep) == 12

    def test_spawn_predator_adds_to_list(self):
        flock = FlockMechanic()
        state = flock.new_state()
        flock.spawn_predator(state, "wolf")
        assert len(state.predators) == 1
        assert state.predators[0].kind == "wolf"

    def test_tick_increments_counter(self):
        flock = FlockMechanic()
        state = flock.new_state()
        state = flock.tick(state)
        assert state.tick == 1

    def test_sheep_reach_water_when_close(self):
        flock = FlockMechanic(flock_size=3)
        state = flock.new_state()
        for sheep in state.sheep:
            sheep.position = state.water_position
        state = flock.tick(state)
        safe = sum(1 for s in state.sheep if s.safe)
        assert safe > 0

    def test_summary_format(self):
        flock = FlockMechanic()
        state = flock.new_state()
        s = flock.summary(state)
        assert "Flock" in s and "Safe" in s


class TestFaith:
    def test_prayer_increases_faith(self):
        fm = FaithMeter(current=0.0, cap=100.0)
        delta = fm.apply(FaithAction.PRAYER, verbose=False)
        assert delta > 0

    def test_disobey_decreases_faith(self):
        fm = FaithMeter(current=50.0, cap=100.0)
        delta = fm.apply(FaithAction.DISOBEY, verbose=False)
        assert delta < 0

    def test_faith_never_below_zero(self):
        fm = FaithMeter(current=0.0, cap=100.0)
        fm.apply(FaithAction.DISOBEY, verbose=False)
        assert fm.current >= 0.0

    def test_faith_never_above_cap(self):
        fm = FaithMeter(current=98.0, cap=100.0)
        fm.apply(FaithAction.SPARE_ENEMY, verbose=False)
        assert fm.current <= 100.0

    def test_expand_cap(self):
        fm = FaithMeter(cap=100.0)
        fm.expand_cap(25.0)
        assert fm.cap == 125.0

    def test_expand_cap_hard_ceiling(self):
        fm = FaithMeter(cap=100.0)
        fm.expand_cap(500.0)
        assert fm.cap == 200.0

    def test_spirit_gate(self):
        fm = FaithMeter(current=24.0, cap=100.0)
        assert not fm.can_activate_spirit(cost=25.0)
        fm.current = 25.0
        assert fm.can_activate_spirit(cost=25.0)
