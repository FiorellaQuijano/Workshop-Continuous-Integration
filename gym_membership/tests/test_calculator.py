from decimal import Decimal

import pytest

from gym_membership.calculator import (
    INVALID_RESULT,
    calculate_subtotal,
    finalize_total,
)


@pytest.mark.parametrize(
    ("plan", "expected_price"),
    [
        ("BASIC", Decimal("30")),
        ("STANDARD", Decimal("45")),
        ("PREMIUM", Decimal("70")),
        (" basic ", Decimal("30")),
    ],
)
def test_calculate_subtotal_for_valid_plans(plan, expected_price):
    assert calculate_subtotal(plan, None, 1) == expected_price


def test_calculate_subtotal_with_multiple_extras_and_members():
    assert calculate_subtotal(
        "STANDARD",
        ["GROUP_CLASSES", "PERSONAL_TRAINING"],
        4,
    ) == Decimal("340")


def test_calculate_subtotal_accepts_one_extra_as_a_string():
    assert calculate_subtotal("STANDARD", "PERSONAL_TRAINING", 1) == Decimal("70")


@pytest.mark.parametrize(
    ("plan", "extras", "members"),
    [
        ("GOLD", None, 1),
        ("BASIC", ["UNKNOWN_EXTRA"], 1),
        ("BASIC", ["SPA"], 1),
        ("STANDARD", ["SPECIALIZED_PROGRAM"], 1),
        ("BASIC", None, 0),
        ("BASIC", None, -1),
        ("BASIC", None, 1.5),
        ("BASIC", ["GROUP_CLASSES", "GROUP_CLASSES"], 1),
    ],
)
def test_calculate_subtotal_returns_invalid_result_for_invalid_selections(
    plan,
    extras,
    members,
):
    assert calculate_subtotal(plan, extras, members) == INVALID_RESULT


@pytest.mark.parametrize(
    ("amount", "expected_total"),
    [
        (Decimal("10.49"), 10),
        (Decimal("10.50"), 11),
        (Decimal("11.50"), 12),
    ],
)
def test_finalize_total_rounds_half_up(amount, expected_total):
    assert finalize_total(amount) == expected_total


def test_finalize_total_returns_invalid_result_when_cancelled():
    assert finalize_total(Decimal("70.50"), confirmed=False) == INVALID_RESULT


def test_finalize_total_returns_invalid_result_for_invalid_amount():
    assert finalize_total(Decimal("NaN")) == INVALID_RESULT


@pytest.mark.parametrize(
    ("plan", "extras", "members", "expected_total"),
    [
        ("BASIC", None, 1, 30),
        ("STANDARD", ["PERSONAL_TRAINING"], 1, 70),
        ("BASIC", ["SPA"], 1, INVALID_RESULT),
        ("GOLD", None, 1, INVALID_RESULT),
        ("BASIC", None, 0, INVALID_RESULT),
    ],
)
def test_developer_a_workshop_examples(plan, extras, members, expected_total):
    subtotal = calculate_subtotal(plan, extras, members)
    assert finalize_total(subtotal) == expected_total
