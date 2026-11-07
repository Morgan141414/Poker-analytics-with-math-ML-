"""Texas Hold'em hand evaluator for five to seven cards."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import Iterable

from .cards import Card, parse_cards

CATEGORY_NAMES = ("high_card", "one_pair", "two_pair", "three_of_a_kind", "straight", "flush", "full_house", "four_of_a_kind", "straight_flush", "royal_flush")


class HandCategory(IntEnum):
    """The ten standard poker hand categories in increasing strength order."""

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


@dataclass(frozen=True, order=True)
class HandValue:
    """Comparable hand strength; higher category and tiebreakers win."""

    category: HandCategory
    tiebreak: tuple[int, ...]

    @property
    def category_name(self) -> str:
        return CATEGORY_NAMES[int(self.category)]

    @property
    def score(self) -> tuple[int, ...]:
        return (int(self.category), *self.tiebreak)


def _straight_high(ranks: Iterable[int]) -> int | None:
    unique = set(ranks)
    if 14 in unique:
        unique.add(1)
    runs = sorted(unique)
    best = None
    for low in runs:
        if all(low + i in unique for i in range(5)):
            best = low + 4
    return best


def evaluate_five(cards: Iterable[Card]) -> HandValue:
    """Evaluate exactly five cards, returning a comparable ``HandValue``."""
    hand = tuple(cards)
    if len(hand) != 5:
        raise ValueError("evaluate_five requires exactly five cards")
    ranks = [c.rank for c in hand]
    counts: dict[int, int] = {}
    for rank in ranks:
        counts[rank] = counts.get(rank, 0) + 1
    flush = len({c.suit for c in hand}) == 1
    straight = _straight_high(ranks)
    if straight and flush:
        return HandValue(HandCategory.ROYAL_FLUSH if straight == 14 else HandCategory.STRAIGHT_FLUSH, (straight,))
    groups = sorted(((count, rank) for rank, count in counts.items()), reverse=True)
    if groups[0][0] == 4:
        return HandValue(HandCategory.FOUR_OF_A_KIND, (groups[0][1], groups[1][1]))
    if groups[0][0] == 3 and groups[1][0] == 2:
        return HandValue(HandCategory.FULL_HOUSE, (groups[0][1], groups[1][1]))
    if flush:
        return HandValue(HandCategory.FLUSH, tuple(sorted(ranks, reverse=True)))
    if straight:
        return HandValue(HandCategory.STRAIGHT, (straight,))
    if groups[0][0] == 3:
        kickers = sorted((r for r in ranks if r != groups[0][1]), reverse=True)
        return HandValue(HandCategory.THREE_OF_A_KIND, (groups[0][1], *kickers))
    pairs = sorted((r for r, count in counts.items() if count == 2), reverse=True)
    if len(pairs) == 2:
        kicker = next(r for r, count in counts.items() if count == 1)
        return HandValue(HandCategory.TWO_PAIR, (pairs[0], pairs[1], kicker))
    if len(pairs) == 1:
        pair = pairs[0]
        return HandValue(HandCategory.ONE_PAIR, (pair, *sorted((r for r in ranks if r != pair), reverse=True)))
    return HandValue(HandCategory.HIGH_CARD, tuple(sorted(ranks, reverse=True)))


def evaluate(cards: Iterable[Card] | str) -> HandValue:
    """Evaluate the best five-card hand from five, six, or seven cards."""
    hand = parse_cards(cards)
    if not 5 <= len(hand) <= 7:
        raise ValueError("evaluate requires between five and seven cards")
    return max(evaluate_five(combo) for combo in combinations(hand, 5))


def category_name(value: HandValue) -> str:
    """Return the human-readable category name for an evaluated hand."""
    return value.category_name


def evaluate_hand(cards: Iterable[Card] | Iterable[str] | str) -> HandValue:
    """Compatibility entry point accepting card objects or compact strings."""
    return evaluate(parse_cards(cards))
