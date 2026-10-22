
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
import pytest


from gym_membership.discounts import (
    group_discount,
    special_offer,
    premium_surcharge,
)

def test_group_discount():
    assert group_discount(100, 1) == 100
    assert group_discount(100, 2) == pytest.approx(90)
    assert group_discount(200, 3) == pytest.approx(180)


def test_special_offer():
    assert special_offer(200) == 200
    assert special_offer(201) == 181
    assert special_offer(400) == 380
    assert special_offer(401) == 351



def test_premium_surcharge():
    assert premium_surcharge(100, False) == 100
    assert premium_surcharge(100, True) == pytest.approx(115)
    assert premium_surcharge(200, True) == pytest.approx(230)


