# Nomad Pizza — Public Order Flow Automation

Automated UI tests for the public customer ordering experience of **Nomad Pizza**, a web application designed around the needs of a local business.

I built the interface and used it to identify the customer journeys and behaviors most valuable to validate with automation. This repository contains the public order-flow tests. Tests for the private interface are maintained separately and are not published for confidentiality.

## Project overview

The suite uses **Python, pytest, Selenium, and the Page Object Model** to validate key customer journeys from menu browsing through order confirmation. Shared test data and pytest parametrization let the same test logic cover multiple products, order types, and ingredient combinations without duplicating scripts.

### Coverage

- **Menu:** product visibility and names, quantity controls, order type, prices, promotions, and customizable pizza ingredients.
- **Customizable pizzas:** ingredient selection, combinations, and price adjustments based on selected ingredients.
- **Cart:** product details, quantity changes, item subtotals, order total, removal confirmation, navigation, and bank-transfer information.
- **Order information:** order ID, customer and payment details, product summary, total, ticket URL and QR code, transfer details, and WhatsApp link.

Menu and cart tests stop before submitting an order. Order-information tests submit a test order and are guarded to run only against Firebase Hosting Emulator on port `5000`.

## Technology and design

- **Python** — test implementation and shared test data.
- **pytest** — fixtures, parametrization, and test execution.
- **Selenium WebDriver** — browser-based UI interactions and assertions.
- **Page Object Model** — page-specific locators and actions are organized under `page_objects/`.
- **Data-driven scenarios** — products, ingredients, and order details are centralized in `data.py` and reused across tests.
- **Firebase Emulator Suite** — isolates order creation from the production Firestore database during end-to-end checkout tests.

## Requirements

- Python 3.10 or later.
- Google Chrome.
- The public Nomad Pizza application, either at a compatible public URL or through the local Firebase Hosting Emulator.
- For `tests/test_info.py`, Firebase Auth, Firestore, and Hosting Emulators must be running with the required test catalog data available.

## Setup

From the repository directory, create a virtual environment and install the test dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The suite defaults to the local customer-facing URL:

```text
http://127.0.0.1:5000/
```

To override it for menu and cart tests, set `NOMAD_PUBLIC_URL` in the current PowerShell session:

```powershell
$env:NOMAD_PUBLIC_URL = "https://your-public-site.example/"
```

This project is for the **public customer interface**. Configure the URL at the site root; do not use `/admin.html` or an Admin URL. The fixtures reject non-root paths, and the order-information tests additionally require the local Hosting Emulator.

## Running the tests

Run individual modules:

```powershell
python -m pytest tests/test_menu.py -v
python -m pytest tests/test_cart.py -v
```

Order-information tests create a test order. Start Firebase Emulators first, then run this module:

```powershell
python -m pytest tests/test_info.py -v
```

To run the full suite, use the same local emulator setup because it includes the order-creation tests:

```powershell
python -m pytest -v
```

Orders created by the end-to-end tests remain in the Firestore Emulator until its local data is cleared. They are not written to Cloud Firestore and are not automatically deleted by this test suite. Do not run order-creation tests against the production site.

## Repository contents

```text
public-order-flow/
├── docs/
│   └── defects/             # Public defect reports and their index
├── page_objects/            # Shared and page-specific Selenium abstractions
├── tests/                   # Menu, cart, and order-information tests
├── conftest.py              # Browser and page-object fixtures
├── data.py                  # URLs and reusable parametrized test data
├── pytest.ini               # pytest defaults
├── requirements.txt         # Python test dependencies
├── test_cases_nomad_pizza.xlsx
├── NOMAD-REQ-DOC-001-EN.pdf
└── README.md
```

## Test cases and defect reports

- [Test case catalog](test_cases_nomad_pizza.xlsx)
- [Public requirements document](NOMAD-REQ-DOC-001-EN.pdf)
- [Defect report index](docs/defects/README.md)

The defect reports document findings from earlier test runs for traceability. They do not necessarily represent the current application state; rerun the related scenarios to confirm whether an issue is still reproducible.

## Scope and confidentiality

Only the public customer-ordering automation is included here. The application source code, private-interface tests, credentials, environment files, and Firestore cleanup integrations are not part of this repository.
