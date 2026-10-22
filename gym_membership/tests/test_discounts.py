
"""
DEVELOPER B - UNIT TESTS
Requirements: R4, R5, R6

Test cases to implement:

R4 - Group Discount:
- 1 member -> no discount.
- 2 or more members -> 10% discount.

R5 - Special Offer:
- Amount = 200 -> no discount.
- Amount = 201 -> subtract 20.
- Amount = 400 -> subtract 20.
- Amount = 401 -> subtract 50.
- Discounts must not accumulate.

R6 - Premium Surcharge:
- Without premium extras -> no surcharge.
- With premium extras -> add 15%.
- Verify surcharge is applied after discounts.

Integration:
- Test the correct calculation order:
  subtotal -> group discount -> special offer
  -> premium surcharge.
- Do not round intermediate results.

Required integration tests:
- BASIC, GROUP_CLASSES, 2 members -> 81.
- BASIC, GROUP_CLASSES, 3 members -> 122.

Note:
- Coordinate with the team on PREMIUM expected
  results due to inconsistencies in the workshop
  example table.

Run tests using:
    python -m pytest -v
"""
from decimal import Decimal

from gym_membership.discounts import (
    group_discount,
    special_offer,
    premium_surcharge,
)


def test_group_discount():
    """Discount group totals by ten percent for two or more members."""
    assert group_discount(Decimal("100"), 1) == Decimal("100")
    assert group_discount(Decimal("100"), 2) == Decimal("90")
    assert group_discount(Decimal("200"), 3) == Decimal("180")


def test_special_offer():
    """Apply the correct exclusive offer at each amount threshold."""
    assert special_offer(Decimal("200")) == Decimal("200")
    assert special_offer(Decimal("201")) == Decimal("181")
    assert special_offer(Decimal("400")) == Decimal("380")
    assert special_offer(Decimal("401")) == Decimal("351")


def test_premium_surcharge():
    """Add fifteen percent only when a premium extra is selected."""
    assert premium_surcharge(Decimal("100"), False) == Decimal("100")
    assert premium_surcharge(Decimal("100"), True) == Decimal("115")
    assert premium_surcharge(Decimal("200"), True) == Decimal("230")


def test_discounts_accept_integer_amounts():
    """Accept integer amounts while retaining exact decimal arithmetic."""
    assert group_discount(100, 2) == Decimal("90")
    assert special_offer(201) == Decimal("181")
    assert premium_surcharge(100, True) == Decimal("115")
