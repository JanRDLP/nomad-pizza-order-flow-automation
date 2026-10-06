from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Comportamiento Selenium compartido por las páginas."""

    def __init__(self, driver, timeout=15):
        """Guarda el navegador y crea la espera explícita común."""
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visible(self, locator):
        """Espera hasta que el elemento localizado sea visible."""
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_until_visible(self, locator):
        """Espera la visibilidad de un localizador sin exponer el WebElement al test."""
        self.wait.until(ec.visibility_of_element_located(locator))

    def clickable(self, locator):
        """Espera hasta que el elemento localizado se pueda pulsar."""
        return self.wait.until(ec.element_to_be_clickable(locator))

    def click(self, locator):
        """Centra el elemento en la ventana antes de pulsarlo para evitar overlays fijos."""
        element = self.clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        self.clickable(locator).click()

    def text(self, locator):
        """Obtiene el texto de un elemento visible."""
        return self.visible(locator).text

    def find_all(self, locator):
        """Devuelve todos los elementos que coinciden con un localizador."""
        return self.driver.find_elements(*locator)

    def is_displayed(self, locator):
        """Indica si existe un elemento que esté visible para el usuario."""
        elements = self.find_all(locator)
        return bool(elements and elements[0].is_displayed())

    def is_visible(self, locator):
        """Indica si el elemento llega a mostrarse dentro del tiempo de espera."""
        try:
            return self.visible(locator).is_displayed()
        except TimeoutException:
            return False
