# NP-3 — Cart order-type assertion failed because the displayed label used uppercase text

- **Related test case:** NO-014 — Cart | Product details match the menu
- **Jira priority:** High
- **Jira status when captured:** Finalizada
- **Report classification:** Case-sensitive test assertion; a functional application defect has not been confirmed.

## Description

The test expected “En sitio,” while the cart returned “EN SITIO.” Both values represent the same order type, but the exact-string assertion failed. The current test compares the values without case sensitivity.

## Steps to reproduce

1. Open the public menu.
2. Select **“En sitio”** (Dine in).
3. Add a product, such as 7up, to the cart.
4. Compare the selected order type with the cart badge.

## Expected result

The cart badge represents the order type selected in the menu.

## Actual result

The test expected “En sitio” and received “EN SITIO.” The values differ only in capitalization. The current assertion uses a case-insensitive comparison; rerun NO-014 to verify the update.

## Test environment

Public order flow served by the Firebase Hosting Emulator at `http://127.0.0.1:5000/`; Google Chrome 154.0.8037.59; Python, pytest, and Selenium.
