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

## Project structure

The public interface requirements and the NO-001–NO-023 test case catalog are documented in English in the files below.

```text
public-order-flow/
├── conftest.py
├── data.py
├── NOMAD-PUBLIC-REQ-DOC-001.docx
├── casos_prueba_nomad_pizza.xlsx
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
