# NP-1 — Pizza Dog takeout promotion is not reflected in the automated menu test

- **Related test case:** NO-007 — Menu | Pizza Dog takeout promotion
- **Jira priority:** Highest
- **Jira status when captured:** Finalizada
- **Report classification:** Promotion/price mismatch observed in automation; an application defect has not been confirmed.

## Description

When the test selects takeout and adds two Pizza Dogs, the 2-for-$100 promotion is expected to apply. In the reported automated run, the test read $120 instead. In another run, the promotion badge did not reach the expected state. Manual verification showed the $100 promotion, so the failure may involve synchronization between the automated order-type selection and the menu.

## Steps to reproduce

1. Open the public menu.
2. Select **“Para llevar”** (Takeout).
3. Set the Pizza Dog quantity to 2.
4. Check the promotion badge and displayed price.

## Expected result

The promotion badge is displayed, and the price for two Pizza Dogs is $100.

## Actual result

The automated run read $120 or did not detect the promotion badge. Manual verification showed the expected $100 promotion.

## Test environment

Public order flow served by the Firebase Hosting Emulator at `http://127.0.0.1:5000/`; Google Chrome 154.0.8037.59; Python, pytest, and Selenium.
