"""Simple action recommendation from equity, pot odds, and raise assumptions."""

from __future__ import annotations

from typing import Literal

from .odds import call_ev, pot_odds, raise_ev

Action = Literal["CALL", "FOLD", "RAISE"]


def recommend_action(equity: float, pot: float, call_amount: float, *, raise_amount: float = 0.0, fold_equity: float = 0.0, raise_threshold: float = 0.05) -> Action:
    """Recommend ``FOLD``, ``CALL``, or ``RAISE`` using a transparent EV rule.

    A raise is selected when its estimated EV exceeds call EV by
    ``raise_threshold * pot``; otherwise a profitable call is selected.
    """
    if not 0 <= equity <= 1 or pot < 0 or call_amount < 0 or raise_amount < 0 or not 0 <= fold_equity <= 1:
        raise ValueError("invalid equity, amounts, or fold equity")
    c_ev = call_ev(equity, pot, call_amount)
    if c_ev < 0:
        return "FOLD"
    if raise_amount > 0 and raise_ev(equity, pot, raise_amount, fold_equity) > c_ev + raise_threshold * pot:
        return "RAISE"
    return "CALL"


def should_call(equity: float, pot: float, call_amount: float) -> bool:
    """Return whether equity clears the pot-odds break-even point."""
    return equity >= pot_odds(call_amount, pot)
