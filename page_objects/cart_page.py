from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class CartPage(BasePage):
    """Acciones y lecturas disponibles en la pantalla del carrito."""
    SCREEN = (By.ID, "pantalla-carrito")
    CLIENT_NAME = (By.ID, "nombre-cliente")
    TOTAL = (By.CSS_SELECTOR, "[data-testid='carrito-total']")
    PAYMENT_METHOD = (By.ID, "metodo-pago")
    PAYMENT_DETAILS = (By.ID, "wrapper-calculadora-efectivo")
    MENU_SCREEN = (By.ID, "pantalla-menu")
    TRANSFER_DETAILS = (By.CSS_SELECTOR, "#wrapper-calculadora-efectivo > div")
    DELETE_CONFIRMATION = (By.ID, "confirmar-eliminacion-carrito")
    DELETE_CONFIRMATION_MESSAGE = (By.ID, "confirmar-eliminacion-mensaje")
    DELETE_ACCEPT = (By.ID, "aceptar-eliminacion-carrito")
    DELETE_CANCEL = (By.ID, "cancelar-eliminacion-carrito")
    BACK = (By.ID, "btn-cancelar-pedido")
    CONTINUE = (By.ID, "btn-continuar-pedido")

    @staticmethod
    def row(product_id, details=None, consume_type=None):
        """Construye el localizador de una línea específica del carrito."""
        selector = f"[data-testid='carrito-item'][data-producto='{product_id}']"
        if details is not None:
            selector += f"[data-detalles='{details}']"
        if consume_type is not None:
            selector += f"[data-consumo='{consume_type}']"
        return By.CSS_SELECTOR, selector

    @classmethod
    def row_part(cls, part, product_id, details=None, consume_type=None):
        """Localiza una parte de la línea, como nombre, cantidad o subtotal."""
        row = cls.row(product_id, details, consume_type)[1]
        return By.CSS_SELECTOR, f"{row} [data-testid='carrito-{part}']"

    @classmethod
    def quantity_locator(cls, product_id, details=None, consume_type=None):
        """Devuelve el localizador del contador de una línea."""
        return cls.row_part("cantidad", product_id, details, consume_type)

    @classmethod
    def increase_button_locator(cls, product_id, details=None, consume_type=None):
        """Devuelve el localizador del botón para aumentar la cantidad."""
        return cls.row_part("mas", product_id, details, consume_type)

    @classmethod
    def decrease_button_locator(cls, product_id, details=None, consume_type=None):
        """Devuelve el localizador del botón para disminuir la cantidad."""
        return cls.row_part("menos", product_id, details, consume_type)

    def product_quantity(self, product_id, details=None, consume_type=None):
        """Lee como texto la cantidad de una línea del carrito."""
        return self.text(self.quantity_locator(product_id, details, consume_type))

    # Lee el contador como entero
    def get_quantity(self, product_id, details=None, consume_type=None):
        """Lee como entero la cantidad de una línea del carrito."""
        return int(self.text(self.quantity_locator(product_id, details, consume_type)))

    # Aumenta en uno la cantidad de un renglón y espera el nuevo valor
    def increase_quantity(self, product_id, details=None, consume_type=None):
        """Aumenta en uno y espera a que el contador refleje el cambio."""
        current = self.get_quantity(product_id, details, consume_type)
        expected = current + 1
        self.click(self.increase_button_locator(product_id, details, consume_type))
        self.wait.until(
            lambda _driver: int(
                self.get_quantity(product_id, details, consume_type)
            ) == expected
        )
        return expected

    # Disminuye en uno; requiere cantidad mayor a uno para evitar el diálogo de eliminar
    def decrease_quantity(self, product_id, details=None, consume_type=None):
        """Disminuye en uno si la cantidad es mayor que uno."""
        current = self.get_quantity(product_id, details, consume_type)
        if current <= 1:
            raise ValueError(
                "La app pide confirmar la eliminación cuando la cantidad es 1. "
                "Usa la acción de eliminar o prueba la resta desde una cantidad mayor a 1."
            )

        expected = current - 1
        self.click(self.decrease_button_locator(product_id, details, consume_type))
        self.wait.until(
            lambda _driver: int(
                self.get_quantity(product_id, details, consume_type)
            ) == expected
        )
        return expected

    def product_subtotal(self, product_id, details=None, consume_type=None):
        """Obtiene el subtotal mostrado para una línea."""
        return self.text(self.row_part("subtotal", product_id, details, consume_type))

    def product_name(self, product_id, details=None, consume_type=None):
        """Obtiene el nombre del producto mostrado en el carrito."""
        return self.text(self.row_part("nombre", product_id, details, consume_type))

    def product_description(self, product_id, details=None, consume_type=None):
        """Obtiene la descripción de una línea del carrito."""
        return self.text(self.row_part("descripcion", product_id, details, consume_type))

    def product_ingredients(self, product_id, details=None, consume_type=None):
        """Obtiene los ingredientes personalizados si aparecen en la línea."""
        locator = self.row_part("ingredientes", product_id, details, consume_type)
        elements = self.find_all(locator)
        return elements[0].text if elements else ""

    def product_consume_type(self, product_id, details=None, consume_type=None):
        """Obtiene el tipo de consumo indicado para el producto."""
        return self.text(self.row_part("consumo", product_id, details, consume_type))

    def row_count(self, product_id, details=None, consume_type=None):
        """Cuenta las líneas que coinciden con el producto y sus detalles."""
        return len(self.find_all(self.row(product_id, details, consume_type)))

    def select_payment_method(self, method):
        """Selecciona la forma de pago indicada."""
        Select(self.visible(self.PAYMENT_METHOD)).select_by_visible_text(method)

    def fill_client_name(self, name):
        """Escribe el nombre del cliente en el formulario del carrito."""
        self.visible(self.CLIENT_NAME).send_keys(name)

    def continue_order(self):
        """Confirma los datos del carrito para continuar el pedido."""
        self.click(self.CONTINUE)

    def resolve_delete_confirmation(self, accept):
        """Acepta o cancela la confirmación para eliminar un producto."""
        self.click(self.DELETE_ACCEPT if accept else self.DELETE_CANCEL)

    def transfer_details(self):
        """Obtiene el texto de los datos bancarios visibles."""
        return self.text(self.TRANSFER_DETAILS)

    def payment_details_text(self):
        """Devuelve los detalles de pago o texto vacío si no aplican."""
        elements = self.find_all(self.PAYMENT_DETAILS)
        return elements[0].text if elements else ""

    def menu_is_visible(self):
        """Indica si la pantalla de menú está visible."""
        return self.is_visible(self.MENU_SCREEN)

    def cart_is_visible(self):
        """Indica si la pantalla del carrito está visible."""
        return self.is_visible(self.SCREEN)

    def total(self):
        """Obtiene el total general que muestra el carrito."""
        return self.text(self.TOTAL)

    def remove_product(self, product_id, details=None, consume_type=None):
        """Elimina del carrito la línea identificada por sus datos."""
        self.click(self.row_part("eliminar", product_id, details, consume_type))
