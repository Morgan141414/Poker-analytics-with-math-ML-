"""Contract tests for poker hand evaluation.

Cards use the compact notation ``[rank][suit]`` (for example, ``As``).
The evaluator is expected to expose ``evaluate_hand(cards)`` and return an
object whose ``category`` is a ``HandCategory`` member (or the corresponding
category name).
"""

import pytest

from poker.evaluator import HandCategory, evaluate_hand


CASES = [
    ("high card", ["As", "Kd", "9c", "7h", "3s"], "HIGH_CARD"),
    ("one pair", ["As", "Ad", "9c", "7h", "3s"], "ONE_PAIR"),
    ("two pair", ["As", "Ad", "9c", "9h", "3s"], "TWO_PAIR"),
    ("three of a kind", ["As", "Ad", "Ac", "9h", "3s"], "THREE_OF_A_KIND"),
    ("straight", ["5s", "4d", "3c", "2h", "As"], "STRAIGHT"),
    ("flush", ["As", "Js", "9s", "5s", "2s"], "FLUSH"),
    ("full house", ["As", "Ad", "Ac", "9h", "9s"], "FULL_HOUSE"),
    ("four of a kind", ["As", "Ad", "Ac", "Ah", "9s"], "FOUR_OF_A_KIND"),
    ("straight flush", ["9s", "8s", "7s", "6s", "5s"], "STRAIGHT_FLUSH"),
    ("royal flush", ["As", "Ks", "Qs", "Js", "Ts"], "ROYAL_FLUSH"),
]


def category_name(value):
    """Allow enum members or string-valued category implementations."""
    category = getattr(value, "category", value)
    return getattr(category, "name", str(category).upper()).upper()


@pytest.mark.parametrize("label,cards,expected", CASES, ids=[case[0] for case in CASES])
def test_all_holdem_categories_are_recognised(label, cards, expected):
    assert category_name(evaluate_hand(cards)) == expected


def test_category_order_is_stronger_than_previous_category():
    assert HandCategory.HIGH_CARD < HandCategory.ONE_PAIR < HandCategory.TWO_PAIR
    assert HandCategory.FULL_HOUSE < HandCategory.FOUR_OF_A_KIND < HandCategory.STRAIGHT_FLUSH


def test_ace_low_straight_is_supported():
    result = evaluate_hand(["As", "2d", "3c", "4h", "5s"])
    assert category_name(result) == "STRAIGHT"


def test_same_category_uses_kickers_to_break_ties():
    ace_pair = evaluate_hand(["As", "Ad", "Kc", "9h", "3s"])
    king_pair = evaluate_hand(["Ks", "Kd", "Qc", "9h", "3s"])
    assert ace_pair > king_pair


def test_duplicate_cards_are_rejected():
    with pytest.raises(ValueError):
        evaluate_hand(["As", "As", "Kd", "9c", "7h"])

