"""Playing-card primitives and parsing helpers for Texas Hold'em."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

RANKS = tuple(range(2, 15))
SUITS = ("c", "d", "h", "s")
RANK_TO_CHAR = {**{n: str(n) for n in range(2, 10)}, 10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}
CHAR_TO_RANK = {**{str(n): n for n in range(2, 10)}, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


@dataclass(frozen=True, order=True)
class Card:
    """An immutable card, represented by a rank (2..14) and suit (c/d/h/s)."""

    rank: int
    suit: str

    def __post_init__(self) -> None:
        if self.rank not in RANKS:
            raise ValueError(f"rank must be between 2 and 14: {self.rank!r}")
        if self.suit.lower() not in SUITS:
            raise ValueError(f"suit must be one of {SUITS}: {self.suit!r}")
        object.__setattr__(self, "suit", self.suit.lower())

    def __str__(self) -> str:
        return f"{RANK_TO_CHAR[self.rank]}{self.suit}"

    @classmethod
    def parse(cls, value: str | "Card") -> "Card":
        """Parse a two-character token such as ``As`` or ``td``."""
        if isinstance(value, cls):
            return value
        token = value.strip()
        if len(token) != 2:
            raise ValueError(f"invalid card token: {value!r}")
        rank = CHAR_TO_RANK.get(token[0].upper())
        suit = token[1].lower()
        if rank is None or suit not in SUITS:
            raise ValueError(f"invalid card token: {value!r}")
        return cls(rank, suit)


def deck() -> tuple[Card, ...]:
    """Return all 52 cards in deterministic rank/suit order."""
    return tuple(Card(rank, suit) for rank in RANKS for suit in SUITS)


def parse_cards(cards: str | Iterable[str | Card] | None) -> tuple[Card, ...]:
    """Parse whitespace/comma-separated cards or an iterable of card tokens."""
    if cards is None:
        return ()
    if isinstance(cards, str):
        normalized = cards.replace(",", " ").split()
        if len(normalized) == 1 and len(normalized[0]) > 2 and len(normalized[0]) % 2 == 0:
            normalized = [normalized[0][i:i + 2] for i in range(0, len(normalized[0]), 2)]
        values: Sequence[str | Card] = tuple(normalized)
    else:
        values = tuple(cards)
    result = tuple(Card.parse(card) for card in values)
    if len(set(result)) != len(result):
        raise ValueError("duplicate cards are not allowed")
    return result


def cards_to_str(cards: Iterable[Card]) -> str:
    """Render cards as a space-separated string."""
    return " ".join(map(str, cards))
