# https://leetcode.com/problems/maximize-the-number-of-partitions-after-operations/
"""This was a pretty rough, not especially performant solution, but Leetcode as a whole is so incredibly frustrating
to use and partly forces you to write bad code... I just did not want to extend this misery."""

from typing import Generator
from string import ascii_lowercase

def get_prefix_scores(string: str, number_of_distinct_characters: int) -> list[int]:
    prefix_scores: list[int] = [0]

    last_distinct_characters: set[str] = set()
    for char in string:
        prefix_chain: int = len(last_distinct_characters)
        if char in last_distinct_characters:  # check if it's not a new character for this partition
            prefix_scores.append(prefix_chain)
            continue

        if prefix_chain == number_of_distinct_characters:  # check if this character starts a new partition
            prefix_chain = 0
            prefix_scores.append(prefix_chain)
            last_distinct_characters = set()

        prefix_chain += 1
        last_distinct_characters.add(char)
        prefix_scores.append(prefix_chain)

    return prefix_scores


def max_partitions(string: str, number_of_distinct_characters: int) -> int:
    assert 1 <= len(string) <= 10 ** 4
    assert 1 <= number_of_distinct_characters <= 26

    if number_of_distinct_characters == 26:
        return 1

    prefix_scores: list[int] = get_prefix_scores(string, number_of_distinct_characters)

    # A character switch can cause a change in the number of maximum partitions.
    # We need to choose the character we want to switch, if any. For this we'll check for chains of prefix scores.
    # 1. If the prefix scores are strictly ascending (with resets to 0), then we can't do any better by switching a character
    #    and can therefore return the currently calculated number
    #
    # 2. If the highest prefix score + 1 is <= the number_of_distinct_characters, then we also can't do any better,
    #    as we simply don't have the number of distinct characters required to start a new partition.
    #
    # 3. If there are chains of prefix scores, then it is always optimal to change the 2nd element of such a chain.
    # 3.1. If number_of_distinct_characters <= 13, then we do not need to actually calculate what character we want to
    #      switch to, we can simply assume we found the optimal one, and for internal calculations use a sentinel instead.
    # 3.2. If number_of_distinct_characters > 13, then we can't just use a sentinel value, as that could lead to an
    #      accidental count of an invalid partition.
    # 3.3. If number_of_distinct_characters == 25, then it is also required to check the string's start as a possible
    #      change index

    if prefix_scores_strictly_ascending(prefix_scores) or max(prefix_scores) + 1 <= number_of_distinct_characters:
        return prefix_scores.count(0)

    max_number_of_partitions: int = prefix_scores.count(0)

    for change_idx in find_possible_character_indices_for_changing(prefix_scores, number_of_distinct_characters == 25):
        changed_prefix_scores_partitions = get_max_number_of_partitions_from_index_change(
            string, prefix_scores, number_of_distinct_characters, change_idx, number_of_distinct_characters <= 13
        )

        max_number_of_partitions = max(max_number_of_partitions, changed_prefix_scores_partitions)

    return max_number_of_partitions


def get_max_number_of_partitions_from_index_change(string: str, prefix_scores: list[int], number_of_distinct_characters: int, change_idx: int, use_sentinel: bool) -> int:
    partition_start_indices: list[int] = list(find_indices_of_partition_starts(prefix_scores))  # sorted

    def get_number_of_partitions_from_char_change(string: str, change_idx: int, change_char: str) -> int:
        # we don't need to copy the entire string. We can simply strip away all the preceding partitions that this
        # character change can't affect, then add those partitions on top of the score at the end again
        preceding_indices: list[int] = [start_index for start_index in partition_start_indices if
                                        start_index < change_idx]
        changed_string: str = string[(0, *preceding_indices)[-1]:change_idx] + change_char + string[change_idx + 1:]
        changed_prefix_scores: list[int] = get_prefix_scores(changed_string, number_of_distinct_characters)
        return changed_prefix_scores.count(0) + (max(0, len(preceding_indices) - 1))

    if use_sentinel:
        return get_number_of_partitions_from_char_change(string, change_idx, '?')
    else:
        return max(get_number_of_partitions_from_char_change(string, change_idx, char) for char in ascii_lowercase)


def prefix_scores_strictly_ascending(prefix_scores: list[int]) -> bool:
    last_score: int = prefix_scores[0]
    for score in prefix_scores[1:]:
        if score == last_score:
            return False

        last_score = score

    return True


def find_indices_of_partition_starts(prefix_scores: list[int]) -> Generator[int, None, None]:
    encountered_zeros: int = 0

    for idx, current_score in enumerate(prefix_scores):
        if current_score == 0:
            yield idx - encountered_zeros
            encountered_zeros += 1

    return None


def find_possible_character_indices_for_changing(prefix_scores: list[int], include_start: bool) -> Generator[int, None, None]:
    if include_start:
        yield 0

    last_score: int = -1
    chain_ongoing: bool = False
    encountered_zeros: int = 0

    for idx, current_score in enumerate(prefix_scores):
        if current_score == 0:
            encountered_zeros += 1

        if last_score == current_score:
            if not chain_ongoing:
                yield idx - encountered_zeros

            chain_ongoing = True
        else:
            chain_ongoing = False

        last_score = current_score

    return None


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        return max_partitions(s, k)