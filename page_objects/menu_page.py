from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from .base_page import BasePage

class MenuPage(BasePage):
    """Acciones y lecturas disponibles en la pantalla del menú."""
    SCREEN = (By.ID, "pantalla-menu")
    MENU_ITEMS = (By.CSS_SELECTOR, "#pos-menu-compartido .inventory_item[id^='item-']")
    CONSUME_TYPE = (By.ID, "tipo-consumo")
    OPEN_CART = (By.ID, "btn-ver-carrito-top")
    CART_COUNT = (By.ID, "cart-count")
    PIZZA_DOG_PROMO = (By.ID, "promo-pizza_dog")
    PRODUCT_DESCRIPTION = "#item-{} [data-testid='menu-product-description']"
    INGREDIENT_SELECTORS = "#selectores-{} select.ing-sel"

    @staticmethod
    def product_locator(part, product_id):
        """Construye el localizador de una parte de la tarjeta del producto."""
        ids = {
            "container": "item-{}",
            "name": "titulo-{}",
            "price": "precio-{}",
            "plus": "mas-{}",
            "minus": "menos-{}",
            "counter": "cant-display-{}",
            "add": "anadir-{}",
            "add_ingredient": "btn-add-ing-{}",
        }
        return By.ID, ids[part].format(product_id)

    @classmethod
    def ingredient_selectors_locator(cls, product_id):
        """Localiza los selectores de ingredientes de una pizza."""
        return By.CSS_SELECTOR, cls.INGREDIENT_SELECTORS.format(product_id)

    @classmethod
    def counter_plus_locator(cls, product_id):
        """Devuelve el localizador del botón para aumentar el contador."""
        return cls.product_locator("plus", product_id)

    @classmethod
    def counter_minus_locator(cls, product_id):
        """Devuelve el localizador del botón para disminuir el contador."""
        return cls.product_locator("minus", product_id)

    @classmethod
    def counter_value_locator(cls, product_id):
        """Devuelve el localizador del contador visible del producto."""
        return cls.product_locator("counter", product_id)

    # El contenedor del producto se puede ver
    def product_is_visible(self, product_id):
        """Comprueba si la tarjeta del producto aparece en el menú."""
        return self.is_visible(self.product_locator("container", product_id))

    # El nombre del producto se hace presente
    def product_name(self, product_id):
        """Obtiene el nombre que muestra la tarjeta del producto."""
        return self.text(self.product_locator("name", product_id))

    # El precio del producto se hace presente
    def product_price(self, product_id):
        """Obtiene el precio que muestra la tarjeta del producto."""
        return self.text(self.product_locator("price", product_id))

    def product_description(self, product_id):
        """Obtiene la descripción del producto en el menú."""
        locator = (By.CSS_SELECTOR, self.PRODUCT_DESCRIPTION.format(product_id))
        return self.text(locator)

    def get_product_quantity(self, product_id):
        """Lee como entero la cantidad seleccionada en el menú."""
        return int(self.text(self.counter_value_locator(product_id)))

    def wait_until_menu_loaded(self):
        """Espera a que el menú termine de cargar sus tarjetas."""
        self.wait.until(lambda _driver: bool(self.find_all(self.MENU_ITEMS)))

    # Aumenta el contador del producto y espera a que la pantalla refleje el cambio
    def counter_plus(self, product_id):
        """Aumenta una unidad y espera a que cambie el contador."""
        expected = self.get_product_quantity(product_id) + 1
        self.click(self.counter_plus_locator(product_id))
        self.wait.until(
            lambda _driver: self.get_product_quantity(product_id) == expected
        )
        return expected

    # Disminuye el contador (sin bajar de cero) y espera a que la pantalla lo refleje
    def counter_minus(self, product_id):
        """Disminuye una unidad sin permitir que el contador sea negativo."""
        expected = max(0, self.get_product_quantity(product_id) - 1)
        self.click(self.counter_minus_locator(product_id))
        self.wait.until(
            lambda _driver: self.get_product_quantity(product_id) == expected
        )
        return expected

    # Da clic en el botón añadir que agrega la cantidad de producto sumada al carrito
    def add_product(self, product_id, quantity=1):
        """Selecciona la cantidad indicada y agrega el producto al carrito."""
        for _ in range(quantity):
            self.counter_plus(product_id)
        self.confirm_add_product(product_id)

    def confirm_add_product(self, product_id):
        """Agrega al carrito la cantidad ya seleccionada en el menú."""
        self.click(self.product_locator("add", product_id))

    # Selecciona el tipo de consumo
    def choose_consume_type(self, label):
        """Selecciona el tipo de consumo y espera a que quede aplicado."""
        self.wait_until_menu_loaded()
        Select(self.visible(self.CONSUME_TYPE)).select_by_visible_text(label)
        self.wait.until(lambda _driver: self.get_consume_type() == label)

    def get_consume_type(self):
        """Devuelve el tipo de consumo seleccionado actualmente."""
        self.wait_until_menu_loaded()
        return Select(self.visible(self.CONSUME_TYPE)).first_selected_option.text

    def wait_for_pizza_dog_promo(self, visible):
        """Espera a que la etiqueta promocional alcance el estado esperado."""
        condition = (
            ec.visibility_of_element_located(self.PIZZA_DOG_PROMO)
            if visible
            else ec.invisibility_of_element_located(self.PIZZA_DOG_PROMO)
        )
        self.wait.until(condition)
        return visible

    def pizza_dog_promo_state(self):
        """Devuelve diagnóstico de URL, consumo y visibilidad de la promo."""
        promo_elements = self.find_all(self.PIZZA_DOG_PROMO)
        state = {
            "url": self.driver.current_url,
            "consumo": self.get_consume_type(),
            "promo_encontrada": bool(promo_elements),
        }

        if promo_elements:
            promo = promo_elements[0]
            state.update({
                "display_inline": promo.get_dom_attribute("style"),
                "display_calculado": promo.value_of_css_property("display"),
                "visible_para_selenium": promo.is_displayed(),
            })

        return state

    def open_cart(self):
        """Abre el carrito desde el menú."""
        self.click(self.OPEN_CART)

    def get_cart_count(self):
        """Lee el total indicado en el botón superior del carrito."""
        return int(self.text(self.CART_COUNT))

    def wait_for_cart_count(self, expected_count):
        """Espera hasta que el contador del carrito tenga el valor esperado."""
        def count_matches(_driver):
            """Retorna el contador solo cuando coincide con el esperado."""
            current_count = self.get_cart_count()
            return current_count if current_count == expected_count else False

        return self.wait.until(count_matches)

    # Da clic en el botón añadir ingrediente
    def add_ingredient(self, product_id):
        """Agrega un selector adicional de ingrediente a la pizza."""
        self.click(self.product_locator("add_ingredient", product_id))
        self.wait_for_ingredient_selectors(product_id, 2)

    def wait_for_ingredient_selectors(self, product_id, count):
        """Espera hasta que la pizza tenga la cantidad indicada de selectores."""
        locator = self.ingredient_selectors_locator(product_id)
        return self.wait.until(lambda _driver: len(self.find_all(locator)) >= count)

    def choose_ingredient(self, product_id, ingredient, selector_index=0):
        """Selecciona un ingrediente visible en una casilla específica."""
        locator = self.ingredient_selectors_locator(product_id)

        def ingredient_is_available(_driver):
            selectors = self.find_all(locator)
            if len(selectors) <= selector_index:
                return False
            return any(
                option.text == ingredient
                for option in Select(selectors[selector_index]).options
            )

        self.wait.until(ingredient_is_available)
        selectors = self.find_all(locator)
        Select(selectors[selector_index]).select_by_visible_text(ingredient)

    # Selecciona los ingredientes visibles para un producto personalizable
    def set_ingredients(self, product_id, ingredients, max_ingredients=3):
        """Selecciona ingredientes en orden y agrega selectores cuando hacen falta."""
        if not ingredients:
            raise ValueError("Debes seleccionar al menos un ingrediente.")
        if len(ingredients) > max_ingredients:
            raise ValueError(
                f"Se permiten como máximo {max_ingredients} ingredientes; "
                f"se recibieron {len(ingredients)}."
            )

        selectors = self.ingredient_selectors_locator(product_id)
        self.wait.until(lambda _driver: len(self.find_all(selectors)) >= 1)

        for index, ingredient in enumerate(ingredients):
            if index:
                self.add_ingredient(product_id)
                self.wait.until(
                    lambda _driver, count=index + 1:
                    len(self.find_all(selectors)) >= count
                )

            # Espera a que la app cargue las opciones disponibles en este selector.
            def ingredient_is_available(_driver):
                """Espera a que el ingrediente exista entre las opciones."""
                current_selectors = self.find_all(selectors)
                if len(current_selectors) <= index:
                    return False
                return any(
                    option.text == ingredient
                    for option in Select(current_selectors[index]).options
                )

            self.wait.until(ingredient_is_available)
            current_selectors = self.find_all(selectors)
            Select(current_selectors[index]).select_by_visible_text(ingredient)

    # Devuelve las opciones disponibles en una casilla de ingredientes
    def ingredient_options(self, product_id, selector_index=0):
        """Lista las opciones de un selector de ingredientes."""
        selectors = self.find_all(self.ingredient_selectors_locator(product_id))
        return [
            option.text
            for option in Select(selectors[selector_index]).options
        ]

    def wait_for_ingredient_options(self, product_id, selector_index=0):
        """Espera a que una casilla tenga sus opciones de ingredientes cargadas."""
        def options_are_loaded(_driver):
            selectors = self.find_all(self.ingredient_selectors_locator(product_id))
            if len(selectors) <= selector_index:
                return False
            options = [option.text for option in Select(selectors[selector_index]).options]
            return options or False

        return self.wait.until(options_are_loaded)

    # Devuelve los ingredientes elegidos, en el orden de las casillas.
    def selected_ingredients(self, product_id):
        """Devuelve los ingredientes elegidos en el orden de los selectores."""
        selectors = self.find_all(self.ingredient_selectors_locator(product_id))
        return [
            Select(selector).first_selected_option.text
            for selector in selectors
        ]

