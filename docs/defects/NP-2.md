# NP-2 — Pizza Dog description differs between the test data and the cart

- **Related test case:** NO-014 — Cart | Product details match the menu
- **Jira priority:** High
- **Jira status when captured:** Finalizada
- **Report classification:** Test-data/assertion mismatch; an application defect has not been confirmed.

## Description

The automated assertion compared the cart description with a fixed value in the test data. The expected text differed from the description returned by the cart. The cart is expected to show the product description from the menu/catalog, so the fixture may have been outdated.

## Steps to reproduce

1. Open the public menu.
2. Add a Pizza Dog to the cart.
3. Compare the product description in the cart with the description shown for that product in the menu/catalog.

## Expected result

The cart displays the same product description as the menu/catalog.

## Actual result

The test expected: “Masa fermentada con salchicha de res ahumada cubierta de salsa de tomate de la casa y mezcla de quesos.”

The cart returned: “Preparacion de nuestra masa fermentada con salchicha de res ahumada cubierta de nuestra salsa de tomate de la casa y mezcla de quesos.”

The current test obtains the expected description from the menu instead of relying on that fixed string. Rerun NO-014 to confirm the updated assertion.

## Test environment

Public order flow served by the Firebase Hosting Emulator at `http://127.0.0.1:5000/`; Google Chrome 154.0.8037.59; Python, pytest, and Selenium.
