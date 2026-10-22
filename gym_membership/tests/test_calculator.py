"""Unit and integration tests for the membership calculator."""

from decimal import Decimal

import pytest

from gym_membership.calculator import (
    INVALID_RESULT,
    calculate_subtotal,
    calculate_total,
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
    """Calculate the price for every valid membership plan."""
    assert calculate_subtotal(plan, None, 1) == expected_price


def test_calculate_subtotal_with_multiple_extras_and_members():
    """Multiply the plan and selected extras by the member count."""
    assert calculate_subtotal(
        "STANDARD",
        ["GROUP_CLASSES", "PERSONAL_TRAINING"],
        4,
    ) == Decimal("340")


def test_calculate_subtotal_accepts_one_extra_as_a_string():
    """Allow a single extra to be supplied without a collection."""
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
    """Reject unsupported plans, extras, members, and duplicate extras."""
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
    """Round final amounts half up to a whole currency unit."""
    assert finalize_total(amount) == expected_total


def test_finalize_total_returns_invalid_result_when_cancelled():
    """Return the invalid-result sentinel when the quote is declined."""
    assert finalize_total(Decimal("70.50"), confirmed=False) == INVALID_RESULT


def test_finalize_total_returns_invalid_result_for_invalid_amount():
    """Reject non-finite amounts."""
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
    """Verify Developer A's valid and invalid workshop examples."""
    subtotal = calculate_subtotal(plan, extras, members)
    assert finalize_total(subtotal) == expected_total


@pytest.mark.parametrize(
    ("plan", "extras", "members", "expected_total"),
    [
        ("BASIC", ["GROUP_CLASSES"], 2, 81),
        ("BASIC", ["GROUP_CLASSES"], 3, 122),
        ("PREMIUM", ["GROUP_CLASSES", "SPA"], 2, 215),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3, 412),
        (
            "PREMIUM",
            ["SPA", "SPECIALIZED_PROGRAM", "PERSONAL_TRAINING"],
            4,
            626,
        ),
        ("BASIC", ["SPA"], 1, INVALID_RESULT),
    ],
)
def test_calculate_total_integrates_developer_a_and_b(
    plan,
    extras,
    members,
    expected_total,
):
    """Apply both developers' pricing rules in the required order."""
    assert calculate_total(plan, extras, members) == expected_total


def test_calculate_total_returns_invalid_result_when_cancelled():
    """Return the invalid-result sentinel when the complete quote is declined."""
    assert calculate_total("BASIC", None, 1, confirmed=False) == INVALID_RESULT
