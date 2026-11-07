"""Self-contained Texas Hold'em equity calculation used by the UI."""

from __future__ import annotations

import itertools
import random
from collections import Counter

RANKS = "23456789TJQKA"
DECK = [rank + suit for rank in RANKS for suit in "shdc"]


def _five_score(cards: tuple[str, ...]) -> tuple:
    values = sorted((RANKS.index(c[0]) + 2 for c in cards), reverse=True)
    counts = Counter(values)
    groups = sorted(((n, value) for value, n in counts.items()), reverse=True)
    unique = sorted(set(values), reverse=True)
    straight = 0
    if len(unique) == 5:
        if unique[0] - unique[4] == 4: straight = unique[0]
        elif unique == [14, 5, 4, 3, 2]: straight = 5
    flush = len({c[1] for c in cards}) == 1
    if straight and flush: return (8, straight)
    if groups[0][0] == 4: return (7, groups[0][1], groups[1][1])
    if groups[0][0] == 3 and groups[1][0] == 2: return (6, groups[0][1], groups[1][1])
    if flush: return (5, *values)
    if straight: return (4, straight)
    if groups[0][0] == 3: return (3, groups[0][1], *sorted((v for v in values if v != groups[0][1]), reverse=True))
    if groups[0][0] == 2 and groups[1][0] == 2:
        pairs = sorted((groups[0][1], groups[1][1]), reverse=True)
        kicker = next(v for v in values if v not in pairs)
        return (2, *pairs, kicker)
    if groups[0][0] == 2:
        pair = groups[0][1]
        return (1, pair, *sorted((v for v in values if v != pair), reverse=True))
    return (0, *values)


def hand_score(cards: list[str]) -> tuple:
    return max(_five_score(combo) for combo in itertools.combinations(cards, 5))


def calculate_equity(hole: list[str], board: list[str], opponents: int, iterations: int = 1200) -> dict:
    """Monte Carlo equity with a deterministic enough, fast default for study."""
    known = set(hole + board)
    if len(known) != len(hole) + len(board):
        raise ValueError("Обнаружены повторяющиеся карты.")
    deck = [card for card in DECK if card not in known]
    if len(board) == 5:
        iterations = min(iterations, 2500)
    wins = ties = 0
    randomizer = random.Random()
    for _ in range(max(100, iterations)):
        sample = randomizer.sample(deck, opponents * 2 + (5 - len(board)))
        cursor = 0
        opponent_hands = [sample[i:i + 2] for i in range(0, opponents * 2, 2)]
        final_board = board + sample[opponents * 2:]
        player = hand_score(hole + final_board)
        scores = [hand_score(hand + final_board) for hand in opponent_hands]
        best = max([player, *scores])
        if player == best:
            if scores.count(best) == 0: wins += 1
            else: ties += 1
    total = max(100, iterations)
    equity = (wins + ties * 0.5) / total
    # Number of unseen river cards which beat the current made hand, useful as a study hint.
    outs = 0
    if len(board) < 5:
        current = hand_score(hole + board) if len(hole + board) >= 5 else None
        if current is not None:
            for river in deck:
                if hand_score(hole + board + [river]) > current:
                    outs += 1
    return {"equity": equity, "outs": outs, "iterations": total}
