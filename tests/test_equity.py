"""Tests for deterministic equity and outs calculations."""

from poker.equity import calculate_equity, calculate_outs


def test_locked_hand_has_one_hundred_percent_equity():
    equity = calculate_equity(
        hero_cards=["As", "Ad"],
        board=["Ac", "Ah", "2s", "7d", "Kd"],
        villain_cards=["Ks", "Kh"],
    )
    assert equity == 1.0


def test_shared_royal_flush_is_a_split_pot():
    equity = calculate_equity(
        hero_cards=["2c", "3c"],
        board=["As", "Ks", "Qs", "Js", "Ts"],
        villain_cards=["9d", "9h"],
    )
    assert equity == 0.5


def test_equity_is_between_zero_and_one_for_unknown_opponent():
    equity = calculate_equity(
        hero_cards=["As", "Kd"],
        board=["Qs", "7c", "2h"],
        villain_cards=None,
    )
    assert 0.0 <= equity <= 1.0


def test_flush_draw_outs_are_returned_as_cards():
    outs = set(calculate_outs(
        hero_cards=["As", "Ks"],
        board=["Qs", "7s", "2d"],
    ))
    assert {"2s", "3s", "4s", "5s", "6s", "8s", "9s", "Ts", "Js"}.issubset(outs)
    assert "As" not in outs  # already held; outs must come from unseen cards


def test_no_outs_when_the_board_is_already_complete():
    assert calculate_outs(
        hero_cards=["As", "Kd"],
        board=["Qs", "Jc", "Ts", "2d", "3h"],
    ) == []

