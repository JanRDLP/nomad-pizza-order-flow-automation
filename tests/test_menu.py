import pytest

from selenium.common.exceptions import TimeoutException
from data import Dropdown, IngredientCases, Products


MENU_PRODUCTS = [
    product_id
    for product_id, product in Products.ITEMS.items()
    if not product.get("temporal", False)
]

PERSONALIZABLE_PRODUCTS = Products.personalizable_ids()

MAX_INGREDIENTS = IngredientCases.MAX_INGREDIENTS
INGREDIENT_COMBINATIONS = IngredientCases.ALL_COMBINATIONS


@pytest.mark.parametrize("product_id", MENU_PRODUCTS)
def test_product_is_visible_in_menu(menu_page, product_id):
    """NO-001: Comprueba que cada producto parametrizado aparezca en el menú."""
    assert menu_page.product_is_visible(product_id)


@pytest.mark.parametrize("product_id, expected_name",
    [
        ("pizza_dog", "Pizza Dog"),
        ("pizza_nomad", "Pizza Nomad"),
        ("pepsi", "Pepsi"),
    ],)
def test_product_name_in_menu(menu_page, product_id, expected_name):
    """NO-002: Comprueba el nombre de los productos seleccionados en el menú."""
    assert menu_page.product_name(product_id) == expected_name


@pytest.mark.parametrize("product_id", MENU_PRODUCTS)
def test_counter_up(menu_page, product_id):
    """NO-003: Comprueba que el botón más aumente en una unidad el contador."""
    assert menu_page.get_product_quantity(product_id) == 0

    menu_page.counter_plus(product_id)
    assert menu_page.get_product_quantity(product_id) == 1


@pytest.mark.parametrize("product_id", MENU_PRODUCTS)
def test_counter_behavior(menu_page, product_id):
    """NO-003: Comprueba que el contador aumente y luego regrese a cero."""
    assert menu_page.get_product_quantity(product_id) == 0

    menu_page.counter_plus(product_id)
    assert menu_page.get_product_quantity(product_id) == 1

    menu_page.counter_minus(product_id)
    assert menu_page.get_product_quantity(product_id) == 0


@pytest.mark.parametrize("product_id", MENU_PRODUCTS)
@pytest.mark.parametrize("quantity", [1, 2])
@pytest.mark.parametrize("consume_type", Dropdown.CONSUME)
def test_add_each_product_to_cart(menu_page, product_id, quantity, consume_type):
    """NO-004–NO-007: Verifica consumo, cantidades, precios y promoción por producto."""
    assert menu_page.get_cart_count() == 0
    menu_page.choose_consume_type(consume_type)
    actual_consume_type = menu_page.get_consume_type()
    assert actual_consume_type == consume_type

    if product_id == "pizza_dog":
        promo_should_be_visible = consume_type == "Para llevar"
        try:
            promo_is_visible = menu_page.wait_for_pizza_dog_promo(
                promo_should_be_visible
            )
        except TimeoutException as error:
            pytest.fail(
                "La etiqueta de promoción de Pizza Dog no alcanzó el estado esperado. "
                f"Esperada visible: {promo_should_be_visible}. "
                f"Diagnóstico: {menu_page.pizza_dog_promo_state()}. "
                f"Error original: {error.msg}",
                pytrace=True,
            )

        assert promo_is_visible == promo_should_be_visible

    for _ in range(quantity):
        menu_page.counter_plus(product_id)

    product = Products.ITEMS[product_id]
    base_price = product["precio_base"]
    has_takeout_promo = (
        product.get("promo") == "2x100_para_llevar"
        and consume_type == "Para llevar"
    )

    if has_takeout_promo:
        pairs, remainder = divmod(quantity, 2)
        expected_total = pairs * 100 + remainder * base_price
        promo_label = " (Promo)" if quantity >= 2 else ""
    else:
        expected_total = base_price * quantity
        promo_label = ""

    expected_price = f"${expected_total}{promo_label}"
    actual_price = menu_page.product_price(product_id)
    print(
        f"Producto: {product['nombre']} | Cantidad: {quantity} | "
        f"Consumo seleccionado: {actual_consume_type} | "
        f"Precio esperado: {expected_price} | "
        f"Precio mostrado: {actual_price}"
    )
    assert actual_price == expected_price

    menu_page.confirm_add_product(product_id)
    assert menu_page.wait_for_cart_count(quantity) == quantity


@pytest.mark.parametrize("product_id", PERSONALIZABLE_PRODUCTS)
def test_selected_ingredient_is_unavailable_in_other_selectors(menu_page, product_id):
    """NO-008: Comprueba que una selección se excluya de las demás casillas."""
    menu_page.wait_until_menu_loaded()
    first_selector_options = menu_page.wait_for_ingredient_options(product_id)
    assert first_selector_options, f"{product_id} no tiene ingredientes disponibles."

    selected_ingredient = first_selector_options[0]
    menu_page.choose_ingredient(product_id, selected_ingredient)
    menu_page.add_ingredient(product_id)

    other_selector_options = menu_page.wait_for_ingredient_options(
        product_id, selector_index=1
    )
    assert selected_ingredient not in other_selector_options


@pytest.mark.parametrize("product_id", PERSONALIZABLE_PRODUCTS)
@pytest.mark.parametrize(
    "ingredients",
    INGREDIENT_COMBINATIONS,
    ids=lambda combo: "-".join(combo),
)
def test_add_custom_pizza_combinations_to_cart(menu_page, product_id, ingredients):
    """NO-009–NO-010: Verifica combinaciones, precio y agregado de pizzas personalizadas."""
    assert menu_page.get_cart_count() == 0

    menu_page.set_ingredients(product_id, ingredients, MAX_INGREDIENTS)

    assert tuple(menu_page.selected_ingredients(product_id)) == ingredients

    expected_price = (
        Products.ITEMS[product_id]["precio_base"]
        + (len(ingredients) - 1) * Products.EXTRA_INGREDIENT_PRICE
    )
    actual_price = menu_page.product_price(product_id)
    print(
        f"Producto: {Products.ITEMS[product_id]['nombre']} | "
        f"Ingredientes: {' + '.join(ingredients)} | "
        f"Precio esperado: ${expected_price} | Precio mostrado: {actual_price}"
    )
    assert actual_price == f"${expected_price}"

    menu_page.add_product(product_id)
    assert menu_page.wait_for_cart_count(1) == 1
