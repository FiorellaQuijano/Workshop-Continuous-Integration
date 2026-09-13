
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
