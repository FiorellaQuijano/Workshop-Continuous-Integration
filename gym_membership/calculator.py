
"""
DEVELOPER A - MEMBERSHIP CALCULATOR
Requirements: R1, R2, R3, R7

Responsibilities:

R1 - Plans:
- Validate the selected membership plan.
- BASIC: $30 per member.
- STANDARD: $45 per member.
- PREMIUM: $70 per member.
- Reject unknown plans.

R2 - Extras:
- GROUP_CLASSES: $15 per member.
- PERSONAL_TRAINING: $25 per member.
- SPA: $30 per member (PREMIUM only).
- SPECIALIZED_PROGRAM: $40 per member (PREMIUM only).
- Reject unknown or incompatible extras.

R3 - Subtotal:
- Calculate:
  (plan_price + sum(extras_prices)) * members
- Members must be greater than or equal to 1.

R7 - Final Result:
- Apply ROUND_HALF_UP to the final amount.
- Round only after all discounts and surcharges.
- Return -1 for invalid selections or cancellation.

Integration:
- Coordinate with Developer B to apply discounts
  and surcharges before final rounding.
- Keep calculation logic separate from user input.

Tests:
- Implement unit tests in tests/test_calculator.py.
"""
