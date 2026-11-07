"""Monte Carlo Texas Hold'em equity simulation."""

from __future__ import annotations

import random
from typing import Iterable

from .cards import Card, deck, parse_cards
from .equity import EquityResult
from .evaluator import evaluate


def monte_carlo_equity(hero: Iterable[Card] | str, board: Iterable[Card] | str = (), opponents: int = 1, simulations: int = 10_000, seed: int | None = None) -> EquityResult:
    """Estimate showdown equity by uniformly sampling legal deals."""
    hero_cards, board_cards = parse_cards(hero), parse_cards(board)
    if len(hero_cards) != 2 or len(board_cards) > 5 or opponents < 1 or simulations < 1:
        raise ValueError("invalid hero, board, opponents, or simulations")
    used = set(hero_cards + board_cards)
    remaining = [card for card in deck() if card not in used]
    rng = random.Random(seed)
    wins = ties = losses = 0
    for _ in range(simulations):
        sample = rng.sample(remaining, 2 * opponents + 5 - len(board_cards))
        full_board = board_cards + tuple(sample[:5 - len(board_cards)])
        hero_value = evaluate(hero_cards + full_board)
        opponent_values = [evaluate(tuple(sample[i:i + 2]) + full_board) for i in range(5 - len(board_cards), len(sample), 2)]
        best = max(opponent_values)
        if hero_value > best: wins += 1
        elif hero_value == best: ties += 1
        else: losses += 1
    return EquityResult(wins, ties, losses)

