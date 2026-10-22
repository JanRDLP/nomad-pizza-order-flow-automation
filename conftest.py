from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

import pytest
from selenium import webdriver

from data import Links
from page_objects import CartPage, MenuPage, OrderInfoPage


@pytest.fixture
def browser_factory():
    """Crea una instancia aislada de Chrome para cada prueba."""
    browsers = []
    temp_dirs = []

    def create_browser():
        download_dir = TemporaryDirectory(prefix="nomad-public-pytest-")
        temp_dirs.append(download_dir)
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(Path(download_dir.name).resolve()),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )
        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(0)
        browsers.append(browser)
        return browser

    yield create_browser

    for browser in browsers:
        browser.quit()
    for temp_dir in temp_dirs:
        temp_dir.cleanup()


@pytest.fixture
def driver(browser_factory):
    """Proporciona un Chrome nuevo para la prueba actual."""
    return browser_factory()


@pytest.fixture
def public_driver(driver):
    """Abre el menú de cliente y evita ejecutar pruebas en admin.html."""
    configured_url = urlsplit(Links.URL_PUBLIC)
    assert configured_url.path.rstrip("/") == "", (
        "La suite public-order-flow solo debe abrir la interfaz de cliente. "
        "Configura NOMAD_PUBLIC_URL como http://127.0.0.1:5000/; "
        f"el valor actual termina en {configured_url.path!r}."
    )

    driver.get(Links.URL_PUBLIC)
    current_url = urlsplit(driver.current_url)
    assert current_url.path.rstrip("/") == "", (
        "La URL configurada redirigió a una ruta que no es la interfaz pública: "
        f"{driver.current_url}. Revisa NOMAD_PUBLIC_URL."
    )
    return driver


@pytest.fixture
def menu_page(public_driver):
    """Entrega el Page Object del menú público."""
    return MenuPage(public_driver)


@pytest.fixture
def cart_page(public_driver):
    """Entrega el Page Object del carrito público."""
    return CartPage(public_driver)


@pytest.fixture
def order_info_page(public_driver):
    """Entrega el Page Object de la información pública del pedido."""
    return OrderInfoPage(public_driver)
