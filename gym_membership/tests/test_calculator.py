
"""
DEVELOPER A - UNIT TESTS
Requirements: R1, R2, R3, R7

Test cases to implement:

R1 - Plans:
- Valid BASIC, STANDARD and PREMIUM plans.
- Invalid plan (e.g. GOLD) returns -1.

R2 - Extras:
- Valid extras for each membership plan.
- Unknown extras return -1.
- Premium extras with BASIC/STANDARD return -1.

R3 - Subtotal:
- Correct calculation with no extras.
- Correct calculation with multiple extras.
- Correct calculation with multiple members.
- Zero or negative members return -1.

R7 - Final Result:
- Correct ROUND_HALF_UP rounding.
- Invalid selections return -1.
- Cancellation returns -1.

Required integration tests:
- BASIC, no extras, 1 member -> 30.
- STANDARD, PERSONAL_TRAINING, 1 -> 70.
- BASIC, SPA, 1 -> -1.
- GOLD, no extras, 1 -> -1.
- BASIC, no extras, 0 -> -1.

Run tests using:
    python -m pytest -v
"""
