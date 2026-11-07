"""Pot-odds and expected-value calculations."""

from __future__ import annotations


def pot_odds(pot_size: float, call_amount: float) -> float:
    """Return the break-even equity needed to call, as a fraction."""
    if call_amount < 0 or pot_size < 0:
        raise ValueError("amounts cannot be negative")
    if call_amount == 0:
        return 0.0
    return call_amount / (pot_size + call_amount)


def pot_odds_ratio(call_amount: float, pot_before_call: float) -> tuple[float, float]:
    """Return pot-odds ratio as ``(call, pot_before_call)``."""
    if call_amount < 0 or pot_before_call < 0:
        raise ValueError("amounts cannot be negative")
    return call_amount, pot_before_call


def call_ev(equity: float, pot_before_call: float, call_amount: float) -> float:
    """Return call EV measured relative to the decision point."""
    if not 0 <= equity <= 1 or pot_before_call < 0 or call_amount < 0:
        raise ValueError("equity must be in [0, 1] and amounts non-negative")
    return equity * pot_before_call - (1.0 - equity) * call_amount


def expected_value(pot_size: float, call_amount: float, equity: float) -> float:
    """Return call EV using the common pot-size convention."""
    return call_ev(equity, pot_size, call_amount)


def raise_ev(equity: float, pot_before_call: float, raise_amount: float, fold_equity: float = 0.0) -> float:
    """Approximate raise EV, including fold equity and a called-pot payoff."""
    if not 0 <= equity <= 1 or not 0 <= fold_equity <= 1 or pot_before_call < 0 or raise_amount < 0:
        raise ValueError("invalid equity, fold equity, or amount")
    called = 1.0 - fold_equity
    return fold_equity * pot_before_call + called * (equity * (pot_before_call + raise_amount) - (1 - equity) * raise_amount)
