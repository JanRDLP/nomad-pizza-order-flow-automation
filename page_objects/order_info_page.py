from selenium.webdriver.common.by import By

from .base_page import BasePage


class OrderInfoPage(BasePage):
    """Lecturas y acciones de la pantalla de información del pedido."""
    # La pantalla es el elemento exterior; el resumen es su contenido.
    SCREEN = (By.ID, "pantalla-info-pedido")
    SUMMARY = (By.ID, "info-pedido-compartido")
    ORDER_ID = (By.ID, "info-id")
    CUSTOMER = (By.ID, "info-nombre")
    PAYMENT_METHOD = (By.ID, "info-pago")
    TOTAL = (By.ID, "info-total")
    ITEMS = (By.ID, "info-orden-items")
    TRANSFER_DETAILS = (By.ID, "info-transferencia-detalle")
    WHATSAPP_LINK = (By.CSS_SELECTOR, "#info-transferencia-detalle a")
    QR_LINK = (By.ID, "info-qr-link")
    QR_CANVAS = (By.ID, "info-qr-canvas")
    BACK_TO_MENU = (By.ID, "btn-volver-menu-default")

    def order_id(self):
        """Lee el identificador mostrado en el resumen del pedido."""
        return self.text(self.ORDER_ID)

    def total(self):
        """Lee el total numérico mostrado en el resumen."""
        return self.text(self.TOTAL)

    def customer(self):
        """Lee el nombre del cliente asociado al pedido."""
        return self.text(self.CUSTOMER)

    def payment_method(self):
        """Lee la forma de pago mostrada en el resumen."""
        return self.text(self.PAYMENT_METHOD)

    def items_text(self):
        """Obtiene el contenido textual de los productos del pedido."""
        return self.text(self.ITEMS)

    def transfer_details(self):
        """Devuelve los datos bancarios mostrados, si existen."""
        elements = self.find_all(self.TRANSFER_DETAILS)
        return elements[0].text if elements else ""

    def ticket_url(self):
        """Lee el destino del enlace del código QR del ticket."""
        return self.visible(self.QR_LINK).get_attribute("href")

    def whatsapp_url(self):
        """Lee el destino de WhatsApp para enviar el comprobante de transferencia."""
        return self.visible(self.WHATSAPP_LINK).get_attribute("href")

    def screen_is_visible(self):
        """Comprueba sin espera adicional si la pantalla de info está visible."""
        elements = self.find_all(self.SCREEN)
        return bool(elements and elements[0].is_displayed())
