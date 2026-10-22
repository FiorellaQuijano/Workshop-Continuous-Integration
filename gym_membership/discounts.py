
"""
DEVELOPER B - DISCOUNTS AND SURCHARGES
Requirements: R4, R5, R6

Responsibilities:

R4 - Group Discount:
- If members >= 2, apply a 10% discount.
- Otherwise, keep the original amount.

R5 - Special Offer:
- Apply AFTER the group discount.
- If amount > 400, subtract $50.
- Else if amount > 200, subtract $20.
- Otherwise, no discount.
- Discounts are NOT cumulative.

R6 - Premium Surcharge:
- Apply AFTER the special offer.
- If at least one premium extra is selected,
  add a 15% surcharge.
- Premium extras:
  SPA and SPECIALIZED_PROGRAM.

Required calculation order:
1. Receive subtotal from Developer A.
2. Apply group discount (R4).
3. Apply special offer (R5).
4. Apply premium surcharge (R6).
5. Return the amount WITHOUT rounding.

Integration:
- Functions must receive an amount and return
  an amount.
- Developer A handles final rounding (R7).
- Do not implement command-line input/output.

Tests:
- Implement unit tests in tests/test_discounts.py.
"""

def group_discounts(amount, members):
    if members >= 2:
        return amount - (amount * 0.1)
    return amount

def special_offer(amount):
    if amount > 400:
        return amount - 50
    if amount > 200:
        return amount - 20
    return amount


def premium_supercharge(amount, has_premium_extra):
    """R6: Add a 15% surcharge if premium extras are selected."""
    if has_premium_extra:
        return amount * 1.15
    return amount


