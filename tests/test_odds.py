"""Tests for pot odds and call EV."""

import pytest

from poker.odds import expected_value, pot_odds


def test_pot_odds_are_call_divided_by_pot_after_call():
    assert pot_odds(pot_size=100, call_amount=50) == pytest.approx(1 / 3)


def test_pot_odds_are_zero_for_a_free_call():
    assert pot_odds(pot_size=100, call_amount=0) == 0.0


def test_pot_odds_reject_negative_values():
    with pytest.raises(ValueError):
        pot_odds(pot_size=100, call_amount=-1)
    with pytest.raises(ValueError):
        pot_odds(pot_size=-1, call_amount=10)


def test_break_even_equity_has_zero_ev():
    assert expected_value(pot_size=100, call_amount=50, equity=1 / 3) == pytest.approx(0.0)


def test_fifty_percent_equity_makes_a_profitable_call():
    # EV = equity * (pot + call) - call = .5 * 150 - 50 = 25.
    assert expected_value(pot_size=100, call_amount=50, equity=0.5) == pytest.approx(25.0)


def test_equity_must_be_a_probability():
    with pytest.raises(ValueError):
        expected_value(pot_size=100, call_amount=50, equity=-0.01)
    with pytest.raises(ValueError):
        expected_value(pot_size=100, call_amount=50, equity=1.01)

