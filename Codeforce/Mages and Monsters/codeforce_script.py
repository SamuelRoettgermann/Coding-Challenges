# https://codeforces.com/contest/792/problem/F
from __future__ import annotations

import bisect
import logging
import math
import sys
from typing import NamedTuple

log = logging.getLogger(__name__)
log.setLevel(logging.FATAL)


def main():
    j: int = 0  # index of last successful query

    def read_q_and_m_from_terminal() -> tuple[int, int]:
        inputs = sys.stdin.readline().split()
        return int(inputs[0]), int(inputs[1])

    queries, total_mana = read_q_and_m_from_terminal()

    # class Query(NamedTuple):
    #     k: int
    #     a: int
    #     b: int

    def get_all_queries_from_terminal() -> list[tuple[int, int, int]]:
        given_data = [int(x) for x in sys.stdin.read().split()]
        it = iter(given_data)
        return list(zip(it, it, it))

    class Spell(NamedTuple):
        dmg_per_sec: int
        mana_per_sec: int
        damage_to_mana_ratio: float

        @classmethod
        def new(cls, dmg_per_sec: int, mana_per_sec: int):
            return cls(dmg_per_sec=dmg_per_sec, mana_per_sec=mana_per_sec,
                       damage_to_mana_ratio=dmg_per_sec / mana_per_sec)

        def is_worse_combination_of(self, less_efficient: Spell, more_efficient: Spell) -> bool:
            # (self.dmg_per_sec - more_efficient.dmg_per_sec) / (self.mana_per_sec - more_efficient.mana_per_sec)
            #  <= (less_efficient.dmg_per_sec - self.dmg_per_sec) / (less_efficient.mana_per_sec - self.mana_per_sec)

            return (self.dmg_per_sec - more_efficient.dmg_per_sec) * (less_efficient.mana_per_sec - self.mana_per_sec)\
                <= (less_efficient.dmg_per_sec - self.dmg_per_sec) * (self.mana_per_sec - more_efficient.mana_per_sec)

        def __lt__(self, other: tuple):
            raise NotImplementedError("tried to natively compare Spells")
            return self.damage_to_mana_ratio < other.damage_to_mana_ratio

        def __repr__(self) -> str:
            return f"S(dps={self.dmg_per_sec}, mana_ps={self.mana_per_sec}, [dmg/mana={self.damage_to_mana_ratio}])"

    spells: list[Spell] = []

    def learn_spell(a: int, b: int):
        """This is an upgrade of the old learn_spell (now learn_spell2) function. Essentially what this does differently
        is, rather than checking if a new spell has a single better neighbour, this function now checks if a certain
        spell could be more/equally optimal reconstructed from its surrounding spells"""

        new_spell = Spell.new(
            dmg_per_sec=(a + j) % 10 ** 6 + 1, mana_per_sec=(b + j) % 10 ** 6 + 1
        )

        insert_idx = bisect.bisect_left(
            spells, new_spell.damage_to_mana_ratio, key=lambda spell: spell.damage_to_mana_ratio
        )
        spell_at_idx = spells[insert_idx] if insert_idx < len(spells) else None

        if spell_at_idx and new_spell.damage_to_mana_ratio == spell_at_idx.damage_to_mana_ratio:
            if new_spell.dmg_per_sec <= spell_at_idx.dmg_per_sec:
                return

            # we remove the old value rather than re-placing it "in-place", as this allows for a nice generic
            # implementation down the line
            del spells[insert_idx]


        more_efficient = spell_at_idx

        # do not insert new spell if we have an obviously stronger single neighbour spell.
        # However, only a more efficient neighbour (right-hand side) with higher DPS can beat us
        if more_efficient and new_spell.dmg_per_sec <= more_efficient.dmg_per_sec:
            return

        spells.insert(insert_idx, new_spell)

        # prune spells (we can exclude the new node, since we already know it's a new optimum)
        # prune obviously less efficient spells (left-hand side)
        remove_down_to_idx = bisect.bisect_left(
            spells,
            -new_spell.dmg_per_sec,
            key=lambda spell: -spell.dmg_per_sec,
            lo=0,
            hi=insert_idx,
        )
        spells[remove_down_to_idx:insert_idx] = []
        insert_idx = remove_down_to_idx

        # prune less efficient spells (left-hand side)
        while insert_idx >= 2 \
                and spells[insert_idx - 1].is_worse_combination_of(spells[insert_idx - 2], spells[insert_idx]):
            del spells[insert_idx - 1]
            insert_idx -= 1

        # prune more efficient spells (right-hand side)
        while insert_idx < len(spells) - 2 \
                and spells[insert_idx + 1].is_worse_combination_of(spells[insert_idx], spells[insert_idx + 2]):
            del spells[insert_idx + 1]
            # no need to adjust insert_idx, as that happens implicitly

    def learn_spell_old(a: int, b: int):
        """This is an old, deprecated version, but I wanted to leave it in. It's still correct in terms of not throwing,
        away a better spell, but it doesn't necessarily detect a spell that's too weak as such.
        Main reason for leaving it in, is because it uses an alternative, imo easier to intuitively understand approach."""

        def insert_and_prune_less_efficient_spells(new_spell: Spell, insert_idx: int):
            """Will replace all spells that are less efficient and have a worse DPS than our new spell, with that new spell
            If spells was already normalized, this behaves the same as list.insert(insert_idx, new_spell) would"""
            remove_down_to_idx = bisect.bisect_left(
                spells,
                -new_spell.dmg_per_sec,
                key=lambda spell: -spell.dmg_per_sec,
                lo=0,
                hi=insert_idx,
            )
            spells[remove_down_to_idx:insert_idx] = [new_spell]

        new_spell = Spell.new(
            dmg_per_sec=(a + j) % 10 ** 6 + 1, mana_per_sec=(b + j) % 10 ** 6 + 1
        )

        if not spells:
            spells[:] = [new_spell]
            return

        insert_idx = bisect.bisect_left(
            spells, new_spell.damage_to_mana_ratio, key=lambda spell: spell.damage_to_mana_ratio
        )
        spell_at_idx = spells[insert_idx] if insert_idx < len(spells) else spells[-1]

        if new_spell.damage_to_mana_ratio == spell_at_idx.damage_to_mana_ratio:
            # trivial if new.DPS <= old.DPS -> no need to do anything

            if new_spell.dmg_per_sec > spell_at_idx.dmg_per_sec:
                insert_and_prune_less_efficient_spells(
                    new_spell, insert_idx + 1
                )  # +1 to also delete the match

            return

        # If we're here then we DID NOT GET A PERFECT RATIO MATCH. This means 'insert_idx' is currently pointing to
        # the next more efficient spell (reminder: if we're here, spells can't be empty, but can have size 1)

        # Interestingly, 'if insert_idx == 0' implies 'new_spell.dmg_to_mana_ratio() < spell_at_idx.dmg_to_mana_ratio()'
        if insert_idx == 0:
            assert new_spell.damage_to_mana_ratio < spell_at_idx.damage_to_mana_ratio

            # trivial if new.DPS <= least_efficient.DPS -> no need to do anything

            if new_spell.dmg_per_sec > spell_at_idx.dmg_per_sec:
                # add new least efficient / most aggressive / most "mana-wasting" spell - pruning is impossible here
                spells.insert(insert_idx, new_spell)

            return

        # If we're here, then the new spell is either the most efficient spell (i.e. the rightmost spell),
        # or might slot in somewhere in-between.
        # Both scenarios could potentially require pruning to keep our invariants correct, but we only ever need to
        # prune towards the left-hand side, i.e. prune less dmg/mana efficient ones, as pruning more efficient spells
        # never makes sense.

        less_efficient = spells[insert_idx - 1]
        more_efficient = spell_at_idx
        # Important to note: If we're here, then it's still possible for spells to only contain a single spell.
        # If so then 'less_efficient is spells[-1] is more_efficient'.
        assert new_spell.damage_to_mana_ratio > less_efficient.damage_to_mana_ratio

        if (
                less_efficient is spells[-1]  # if new spell is the new most efficient one
                or new_spell.dmg_per_sec > more_efficient.dmg_per_sec  # or it has more DPS than a more efficient one
        ):
            insert_and_prune_less_efficient_spells(new_spell, insert_idx)
            return

        log.warning(f"{new_spell=} did not get added to the spells (silent accidental fall-through?)")

    class MonsterFight(NamedTuple):
        time_limit: int
        hit_points: int

    def can_two_spells_win(spell1: Spell, spell2: Spell, fight: MonsterFight) -> bool:
        # Given:
        # - Two spells (dps1, mps1) and (dps2, mps2)
        # - total_mana as tm
        # - time_limit as tl
        # - target_hp as hp

        dps1, mps1 = spell1.dmg_per_sec, spell1.mana_per_sec
        dps2, mps2 = spell2.dmg_per_sec, spell2.mana_per_sec
        tm = total_mana
        tl = fight.time_limit
        hp = fight.hit_points

        # We want to know:
        # cast times ct1, ct2 elem (0, 1)   [interval notation, i.e. 0 and 1 are exclusive]
        #
        # (1)  ct1 * dps1 + ct2 * dps2  ==  hp
        # (2)  ct1 * mps1 + ct2 * mps2  <=  tm
        # (3)  ct1 + ct2                <=  tl
        #
        # For the following re-arranging, intermediary steps were performed on paper and are omitted here
        #
        # We can re-arrange (1):
        # (1')  ct1  ==  (hp - ct2 * dps2) / dps1
        #
        # and then use that as a substitution in (2) and (3):
        #
        # (2')  (hp - ct2 * dps2) / dps1 * mps1 + ct2 * mps2  <=  tm
        #       ct2                                           <=  (tm * dps1 - hp * mps1) / (dps1 * mps2 - dps2 * mps1)
        #
        # (3')  (hp - ct2 * dps2) / dps1 + ct2  <=  tl
        #       ct2                             <=  (tl * dps1 - hp) / (dps1 - dps2)
        #
        # we choose ct2 so it is the maximum it can be.
        # For example if (2') yields 'ct2 <= 4' and (3') yields 'ct2 <= 2.5', then we would choose ct2 = 2.5
        two_dash_rhs = (tm * dps1 - hp * mps1) / (dps1 * mps2 - dps2 * mps1)
        three_dash_rhs = (tl * dps1 - hp) / (dps1 - dps2)
        ct2 = min(two_dash_rhs, three_dash_rhs)

        # Once that is done, we substitute ct2 by that value in (1') to calculate ct1.
        ct1 = (hp - ct2 * dps2) / dps1

        # Then, to verify everything holds, we plug the ct1 and ct2 values into all 3 (in-)equations and see if they
        # are all satisfied.
        # fmt: off
        # @formatter:off
        return (
                math.isclose(ct1 * dps1 + ct2 * dps2, hp)
            and ct1 * mps1 + ct2 * mps2  <=  tm
            and ct1 + ct2                <=  tl
        )
        # @formatter:on
        # fmt: on

    def is_fight_winnable(a: int, b: int) -> bool:
        fight = MonsterFight(
            time_limit=(a + j) % 10 ** 6 + 1, hit_points=(b + j) % 10 ** 6 + 1
        )

        assert fight.time_limit and fight.hit_points

        if not spells:
            return False

        log.debug(f"\t{fight=} => ")

        dmg_per_mana_required = fight.hit_points / total_mana
        least_efficient_sufficient_dmg_per_mana_spell_idx = bisect.bisect_left(
            spells,
            dmg_per_mana_required,
            key=lambda spell: spell.damage_to_mana_ratio
        )
        if least_efficient_sufficient_dmg_per_mana_spell_idx == len(spells):
            # we'd need a more mana efficient spell than our most efficient one
            return False

        dmg_per_second_required = fight.hit_points / fight.time_limit
        if least_efficient_sufficient_dmg_per_mana_spell_idx == 0:
            # we can try to use our least efficient / most aggressive spell
            return spells[0].dmg_per_sec >= dmg_per_second_required

        assert 0 < least_efficient_sufficient_dmg_per_mana_spell_idx < len(spells)
        # If we're here then we have a "middle-match", i.e. we have at least one spell that would allow us to kill the
        # enemy, given our mana constraint, and we have at least one spell that would run out of mana before killing
        # the enemy.
        least_efficient_sufficient_dmg_per_mana_spell = spells[least_efficient_sufficient_dmg_per_mana_spell_idx]

        if least_efficient_sufficient_dmg_per_mana_spell.dmg_per_sec >= dmg_per_second_required:
            # trivial case, where we just need a single spell
            return True

        # If we're here then our ideal single spell didn't work because it ran out of time.
        # This is where it gets complicated, as we need to somehow factor in the time_limit now.
        # (without accidentally violating the mana constraint in the process).
        most_efficient_non_sufficient_dmg_per_mana_spell = spells[least_efficient_sufficient_dmg_per_mana_spell_idx - 1]
        return can_two_spells_win(most_efficient_non_sufficient_dmg_per_mana_spell,
                                  least_efficient_sufficient_dmg_per_mana_spell,
                                  fight)

    max_number_of_active_spells = 0
    running_count_of_spells = 0
    output = bytearray(4 * queries)  # '4 * queries' is always enough, and in fact, it's always a little too much.
    bytes_written = 0

    log.info(f"{total_mana=}")
    for i, query in enumerate(get_all_queries_from_terminal(), start=1):
        k, a, b = query

        log.info(f"{i=}, {j=}; {query}; Spells = {spells}")
        running_count_of_spells += len(spells)

        if k == 1:
            learn_spell(a, b)
            max_number_of_active_spells = max(max_number_of_active_spells, len(spells))
            continue

        assert k == 2

        if is_fight_winnable(a, b):
            log.debug("\t" * 14 + "YES")
            output[bytes_written: bytes_written + 4] = b"YES\n"
            bytes_written += 4
            j = i
        else:
            log.debug("\t" * 14 + "NO")
            output[bytes_written: bytes_written + 3] = b"NO\n"
            bytes_written += 3

    print(output[:bytes_written].decode('ascii'), end='')
    log.debug(
        f"Most number of spells was {max_number_of_active_spells}. At the very end we had {len(spells)} spells. Average number of spells per iteration was {running_count_of_spells / max(queries, 1):.2f}."
    )


if __name__ == "__main__":
    main()
