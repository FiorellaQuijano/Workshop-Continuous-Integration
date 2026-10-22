"""Developer A's plan validation, subtotal, and final rounding logic."""

from collections.abc import Iterable
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

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


def calculate_subtotal(
    plan: str,
    extras: Iterable[str] | str | None,
    members: int,
) -> Decimal | int:
    """Return the unrounded subtotal, or -1 when the selection is invalid."""
    if not isinstance(plan, str) or type(members) is not int or members < 1:
        return INVALID_RESULT

    selected_plan = plan.strip().upper()
    if selected_plan not in PLAN_PRICES:
        return INVALID_RESULT

    if extras is None:
        selected_extras = ()
    elif isinstance(extras, str):
        selected_extras = (extras,)
    else:
        try:
            selected_extras = tuple(extras)
        except TypeError:
            return INVALID_RESULT

    normalized_extras: list[str] = []
    for extra in selected_extras:
        if not isinstance(extra, str):
            return INVALID_RESULT
        normalized_extra = extra.strip().upper()
        if normalized_extra not in EXTRA_PRICES:
            return INVALID_RESULT
        if normalized_extra in normalized_extras:
            return INVALID_RESULT
        if (
            normalized_extra in PREMIUM_EXTRAS
            and selected_plan != "PREMIUM"
        ):
            return INVALID_RESULT
        normalized_extras.append(normalized_extra)

    per_member_price = PLAN_PRICES[selected_plan] + sum(
        (EXTRA_PRICES[extra] for extra in normalized_extras),
        start=Decimal("0"),
    )
    return per_member_price * members


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
