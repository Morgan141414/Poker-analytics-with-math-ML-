"""Exact showdown equity by enumerating unknown opponents and board cards."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .cards import Card, deck, parse_cards
from .evaluator import evaluate


@dataclass(frozen=True)
class EquityResult:
    """Win/tie/loss counts and probabilities for a hero hand."""

    wins: int
    ties: int
    losses: int
    @property
    def total(self) -> int:
        return self.wins + self.ties + self.losses
    @property
    def win_probability(self) -> float:
        return self.wins / self.total if self.total else 0.0
    @property
    def tie_probability(self) -> float:
        return self.ties / self.total if self.total else 0.0
    @property
    def equity(self) -> float:
        return (self.wins + self.ties / 2) / self.total if self.total else 0.0


def exact_equity(hero: Iterable[Card] | str, board: Iterable[Card] | str = (), opponents: int = 1) -> EquityResult:
    """Enumerate every legal opponent hand and completion board.

    This is exact for the supplied number of uniformly random opponents; it can
    become expensive with many opponents or an empty flop.
    """
    hero_cards = parse_cards(hero)
    board_cards = parse_cards(board)
    if len(hero_cards) != 2 or len(board_cards) > 5 or opponents < 1:
        raise ValueError("hero must contain 2 cards, board 0..5 cards, opponents >= 1")
    used = set(hero_cards + board_cards)
    remaining = tuple(card for card in deck() if card not in used)
    need_board = 5 - len(board_cards)
    wins = ties = losses = 0
    for board_extra in combinations(remaining, need_board):
        full_board = board_cards + board_extra
        available = tuple(card for card in remaining if card not in board_extra)
        hero_value = evaluate(hero_cards + full_board)
        for opponent_hands in combinations(available, 2 * opponents):
            opponent_values = [evaluate(opponent_hands[i:i + 2] + full_board) for i in range(0, 2 * opponents, 2)]
            best = max(opponent_values)
            if hero_value > best:
                wins += 1
            elif hero_value == best:
                ties += 1
            else:
                losses += 1
    return EquityResult(wins, ties, losses)


def calculate_equity(hero_cards: Iterable[Card] | str, board: Iterable[Card] | str = (), villain_cards: Iterable[Card] | str | None = None) -> float:
    """Return hero showdown equity, exactly when villain cards are known or unknown."""
    hero = parse_cards(hero_cards)
    board_cards = parse_cards(board)
    if villain_cards is None:
        return exact_equity(hero, board_cards).equity
    villain = parse_cards(villain_cards)
    if len(villain) != 2 or len(board_cards) > 5:
        raise ValueError("villain must contain 2 cards and board at most 5 cards")
    if len(board_cards) == 5:
        h, v = evaluate(hero + board_cards), evaluate(villain + board_cards)
        return float(h > v) + (0.5 if h == v else 0.0)
    used = set(hero + villain + board_cards)
    remaining = tuple(card for card in deck() if card not in used)
    wins = ties = total = 0
    for extra in combinations(remaining, 5 - len(board_cards)):
        h, v = evaluate(hero + board_cards + extra), evaluate(villain + board_cards + extra)
        wins += h > v
        ties += h == v
        total += 1
    return (wins + ties / 2) / total


def calculate_outs(hero_cards: Iterable[Card] | str, board: Iterable[Card] | str) -> list[str]:
    """Return unseen turn cards that improve the current best hand category."""
    hero, board_cards = parse_cards(hero_cards), parse_cards(board)
    if len(board_cards) >= 5:
        return []
    used = set(hero + board_cards)
    current = evaluate(hero + board_cards) if len(hero + board_cards) >= 5 else None
    outs = []
    for card in deck():
        if card in used:
            continue
        candidate = evaluate(hero + board_cards + (card,))
        if current is None or candidate > current:
            outs.append(str(card))
    return outs

