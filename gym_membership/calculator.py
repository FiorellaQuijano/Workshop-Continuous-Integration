"""Developer A's plan validation, subtotal, and final rounding logic."""

from collections.abc import Iterable
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from gym_membership.discounts import (
    group_discount,
    premium_surcharge,
    special_offer,
)

INVALID_RESULT = -1

PLAN_PRICES = {
    "BASIC": Decimal("30"),
    "STANDARD": Decimal("45"),
    "PREMIUM": Decimal("70"),
}

EXTRA_PRICES = {
    "GROUP_CLASSES": Decimal("15"),
    "PERSONAL_TRAINING": Decimal("25"),
    "SPA": Decimal("30"),
    "SPECIALIZED_PROGRAM": Decimal("40"),
}

PREMIUM_EXTRAS = frozenset({"SPA", "SPECIALIZED_PROGRAM"})


def _normalize_extras(extras: Iterable[str] | str | None) -> tuple[str, ...] | None:
    if extras is None:
        selected_extras = ()
    elif isinstance(extras, str):
        selected_extras = (extras,)
    else:
        try:
            selected_extras = tuple(extras)
        except TypeError:
            return None

    normalized_extras: list[str] = []
    for extra in selected_extras:
        if not isinstance(extra, str):
            return None
        normalized_extra = extra.strip().upper()
        if normalized_extra not in EXTRA_PRICES:
            return None
        if normalized_extra in normalized_extras:
            return None
        normalized_extras.append(normalized_extra)
    return tuple(normalized_extras)


def _subtotal_for_valid_selection(
    selected_plan: str,
    selected_extras: tuple[str, ...],
    members: int,
) -> Decimal:
    per_member_price = PLAN_PRICES[selected_plan] + sum(
        (EXTRA_PRICES[extra] for extra in selected_extras),
        start=Decimal("0"),
    )
    return per_member_price * members


def calculate_subtotal(
    plan: str,
    extras: Iterable[str] | str | None,
    members: int,
) -> Decimal | int:
    """Return the unrounded subtotal, or -1 when the selection is invalid."""
    if (
        not isinstance(plan, str)
        or not isinstance(members, int)
        or isinstance(members, bool)
        or members < 1
    ):
        return INVALID_RESULT

    selected_plan = plan.strip().upper()
    if selected_plan not in PLAN_PRICES:
        return INVALID_RESULT

    normalized_extras = _normalize_extras(extras)
    if normalized_extras is None:
        return INVALID_RESULT

    for normalized_extra in normalized_extras:
        if (
            normalized_extra in PREMIUM_EXTRAS
            and selected_plan != "PREMIUM"
        ):
            return INVALID_RESULT

    return _subtotal_for_valid_selection(selected_plan, normalized_extras, members)


def finalize_total(amount: Decimal | int | float, confirmed: bool = True) -> int:
    """Round the final unrounded amount half up, or return -1 if declined/invalid."""
    if not confirmed or isinstance(amount, bool):
        return INVALID_RESULT

    try:
        final_amount = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError):
        return INVALID_RESULT

    if not final_amount.is_finite() or final_amount == INVALID_RESULT:
        return INVALID_RESULT

    return int(final_amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def calculate_total(
    plan: str,
    extras: Iterable[str] | str | None,
    members: int,
    confirmed: bool = True,
) -> int:
    """Calculate and round a quote after applying the Developer B adjustments."""
    if (
        not isinstance(plan, str)
        or not isinstance(members, int)
        or isinstance(members, bool)
        or members < 1
    ):
        return INVALID_RESULT

    selected_plan = plan.strip().upper()
    if selected_plan not in PLAN_PRICES:
        return INVALID_RESULT

    normalized_extras = _normalize_extras(extras)
    if normalized_extras is None:
        return INVALID_RESULT
    if any(
        extra in PREMIUM_EXTRAS for extra in normalized_extras
    ) and selected_plan != "PREMIUM":
        return INVALID_RESULT

    subtotal = _subtotal_for_valid_selection(selected_plan, normalized_extras, members)
    amount = group_discount(subtotal, members)
    amount = special_offer(amount)
    amount = premium_surcharge(
        amount,
        any(extra in PREMIUM_EXTRAS for extra in normalized_extras),
    )
    return finalize_total(amount, confirmed)
