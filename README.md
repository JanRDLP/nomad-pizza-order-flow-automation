# Nomad Pizza: Public Order Flow Automation

UI automation for Nomad Pizza's public ordering journey. It uses **Python, pytest, and Selenium**, with the Page Object Model and parametrized test data to validate the menu, cart, and public order information.

This repository contains only tests and Page Objects for the public customer experience. Admin interface automation is maintained separately and is not included here for confidentiality. The application source code, credentials, `.env` files, and Firestore cleanup integrations are also excluded.

## Scope

- **Menu:** product visibility and names, quantity counters, order type, prices, and the Pizza Dog promotion.
- **Customizable pizzas:** ingredient availability across selectors, ingredient combinations, and price calculations based on the selected ingredients.
- **Cart:** quantities, line subtotals and order total; confirmation when decreasing a quantity from one to zero; product details; remove and back actions; and bank details when bank transfer is selected.
- **Public order information:** order summary, order ID, customer, payment method, total, products, ticket/QR link, return-to-menu action, and bank transfer/WhatsApp details.

Menu and cart tests stop before submitting an order. The two order information tests create a test order to reach the summary, so they are restricted to the local Firebase Hosting Emulator (port 5000). Orders remain in the Firestore Emulator and are not deleted automatically. The new-order notification test is not included because it belongs to the admin experience.

## Requirements

- Python 3.10 or later.
- Google Chrome.
- An accessible URL for the public application. By default, the tests use Firebase Hosting Emulator at `http://127.0.0.1:5000/`.
- For `test_info.py`, Firebase Auth and Firestore Emulator must also be running, in addition to Hosting Emulator.

## Installation and usage

From this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

To run the tests against a different public URL, set this environment variable for the current terminal session:

```powershell
$env:NOMAD_PUBLIC_URL = "https://your-public-site.example/"
```

Run the public menu and cart tests:

```powershell
python -m pytest tests/test_menu.py tests/test_cart.py -v
```

The order information tests submit local test orders. Run them only while Firebase Emulators are running:

```powershell
python -m pytest tests/test_info.py -v
```

Ingredient combinations are parametrized and may produce many test cases in a run.

## Test Results and Defect Reports

The reports below document findings from earlier test executions. They are kept for traceability and do not necessarily represent current failures; rerun the related cases to confirm their status. The public reports include the observed behavior and test context without requiring access to Jira.

| Jira issue | Test case | Finding |
| --- | --- | --- |
| [NP-1](docs/defects/NP-1.md) | NO-007 | Pizza Dog takeout promotion and price synchronization |
| [NP-2](docs/defects/NP-2.md) | NO-014 | Test data description differs from the menu/cart description |
| [NP-3](docs/defects/NP-3.md) | NO-014 | Order-type label capitalization caused an exact-match assertion failure |

NO-014 is linked to both NP-2 and NP-3 because the reports describe separate observations from the same cart test case.

## Project structure

The NO-001–NO-023 test case catalog and the public defect reports are documented in English in the files below.

```text
public-order-flow/
├── conftest.py
├── data.py
├── casos_prueba_nomad_pizza.xlsx
├── docs/
│   └── defects/
│       ├── NP-1.md
│       ├── NP-2.md
│       ├── NP-3.md
│       └── README.md
├── page_objects/
│   ├── base_page.py
│   ├── cart_page.py
│   ├── menu_page.py
│   ├── order_info_page.py
│   └── __init__.py
├── tests/
│   ├── test_cart.py
│   ├── test_info.py
│   └── test_menu.py
├── pytest.ini
├── requirements.txt
└── README.md
```
