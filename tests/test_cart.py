import pytest

from data import Dropdown, IngredientCases, Products


def add_product_to_cart(menu_page, product_id, quantity=1, consume_type="En sitio"):
    """Agrega un producto desde el menú y deja abierta la pantalla del carrito."""
    menu_page.wait_until_menu_loaded()
    menu_page.choose_consume_type(consume_type)
    menu_page.add_product(product_id, quantity)
    menu_page.open_cart()


@pytest.mark.parametrize("consume_type", Dropdown.CONSUME)
def test_quantity_changes_update_subtotal_and_order_total(menu_page, cart_page, consume_type):
    """NO-011: Comprueba que aumentar o disminuir unidades actualice ambos totales."""
    # Usamos una bebida para que el precio unitario no dependa de promociones.
    add_product_to_cart(menu_page, "7up", 2, consume_type)

    assert cart_page.get_quantity("7up", "Bebida", consume_type) == 2
    assert cart_page.product_subtotal("7up", "Bebida", consume_type) == "$40"
    assert cart_page.total() == "Total: $40"

    cart_page.increase_quantity("7up", "Bebida", consume_type)
    assert cart_page.get_quantity("7up", "Bebida", consume_type) == 3
    assert cart_page.product_subtotal("7up", "Bebida", consume_type) == "$60"
    assert cart_page.total() == "Total: $60"

    cart_page.decrease_quantity("7up", "Bebida", consume_type)
    assert cart_page.get_quantity("7up", "Bebida", consume_type) == 2
    assert cart_page.product_subtotal("7up", "Bebida", consume_type) == "$40"
    assert cart_page.total() == "Total: $40"


@pytest.mark.parametrize("action", ["accept", "cancel"])
def test_decreasing_quantity_from_one_shows_delete_confirmation(menu_page, cart_page, action):
    """NO-012–NO-013: Prueba aceptar o cancelar la eliminación al bajar de uno."""
    add_product_to_cart(menu_page, "7up", 1)

    cart_page.click(cart_page.decrease_button_locator("7up", "Bebida", "En sitio"))
    assert cart_page.visible(cart_page.DELETE_CONFIRMATION).is_displayed()
    assert cart_page.text(cart_page.DELETE_CONFIRMATION_MESSAGE) == "¿Deseas eliminar este producto?"

    if action == "accept":
        cart_page.resolve_delete_confirmation(accept=True)
        cart_page.wait.until(lambda _driver: cart_page.menu_is_visible())
        assert not cart_page.cart_is_visible()
        assert cart_page.row_count("7up", "Bebida", "En sitio") == 0
    else:
        cart_page.resolve_delete_confirmation(accept=False)
        assert cart_page.get_quantity("7up", "Bebida", "En sitio") == 1
        assert cart_page.product_subtotal("7up", "Bebida", "En sitio") == "$20"
        assert cart_page.total() == "Total: $20"


@pytest.mark.parametrize(
    "product_id,consume_type,quantity,details,expected_name,expected_subtotal",
    [
        ("pizza_dog", "Para llevar", 2, "Promoción", "Pizza Dog", "$100"),
        ("7up", "En sitio", 1, "Bebida", "7up", "$20"),
    ],
)
def test_cart_item_matches_product_added_from_menu(menu_page, cart_page, product_id, consume_type, quantity, details,
                                                   expected_name, expected_subtotal,):
    """NO-014: Compara nombre, descripción, consumo, cantidad y precio con el menú."""
    menu_page.wait_until_menu_loaded()
    expected_description = menu_page.product_description(product_id)
    add_product_to_cart(menu_page, product_id, quantity, consume_type)

    assert cart_page.row_count(product_id, details, consume_type) == 1
    assert cart_page.product_name(product_id, details, consume_type) == expected_name
    assert expected_description in cart_page.product_description(
        product_id, details, consume_type
    )
    assert cart_page.product_consume_type(product_id, details, consume_type).casefold() == consume_type.casefold()
    assert cart_page.get_quantity(product_id, details, consume_type) == quantity
    assert cart_page.product_subtotal(product_id, details, consume_type) == expected_subtotal
    assert cart_page.total() == f"Total: {expected_subtotal}"


@pytest.mark.parametrize(
    "product_id",
    Products.personalizable_ids(),
    ids=Products.personalizable_ids(),
)
@pytest.mark.parametrize(
    "ingredients",
    IngredientCases.ALL_COMBINATIONS,
    ids=lambda combo: "-".join(combo),
)
def test_cart_custom_pizza_shows_selected_ingredients(
    menu_page, cart_page, product_id, ingredients
):
    """NO-008–NO-009: Comprueba ingredientes y precio de cada combinación personalizada."""
    ingredients = tuple(ingredients)
    details = " - ".join(ingredients)
    expected_name = f"{Products.ITEMS[product_id]['nombre']} - {len(ingredients)} ing."

    menu_page.wait_until_menu_loaded()
    menu_page.choose_consume_type("En sitio")
    menu_page.set_ingredients(product_id, ingredients)
    menu_page.add_product(product_id)
    menu_page.open_cart()

    assert cart_page.product_name(product_id, details, "En sitio") == expected_name
    assert details in cart_page.product_ingredients(product_id, details, "En sitio")
    expected_price = (
        Products.ITEMS[product_id]["precio_base"]
        + (len(ingredients) - 1) * Products.EXTRA_INGREDIENT_PRICE
    )
    assert cart_page.product_subtotal(product_id, details, "En sitio") == f"${expected_price}"
    assert cart_page.total() == f"Total: ${expected_price}"


def test_remove_button_deletes_product_and_returns_to_menu_when_cart_is_empty(menu_page, cart_page):
    """NO-015: Comprueba que eliminar el último producto vacíe el carrito y vuelva al menú."""
    add_product_to_cart(menu_page, "7up")

    cart_page.remove_product("7up", "Bebida", "En sitio")

    cart_page.wait.until(lambda _driver: cart_page.menu_is_visible())
    assert not cart_page.cart_is_visible()
    assert cart_page.row_count("7up", "Bebida", "En sitio") == 0


def test_remove_button_keeps_other_products_in_cart(menu_page, cart_page):
    """NO-016: Comprueba que eliminar una línea conserve los demás productos."""
    menu_page.wait_until_menu_loaded()
    menu_page.choose_consume_type("En sitio")
    menu_page.add_product("7up", 1)
    menu_page.add_product("agua_jamaica", 1)
    menu_page.open_cart()

    cart_page.remove_product("7up", "Bebida", "En sitio")

    assert cart_page.cart_is_visible()
    assert cart_page.row_count("7up", "Bebida", "En sitio") == 0
    assert cart_page.get_quantity("agua_jamaica", "Bebida", "En sitio") == 1
    assert cart_page.total() == "Total: $20"


def test_back_button_returns_to_menu_and_keeps_cart_contents(menu_page, cart_page):
    """NO-017: Comprueba que volver al menú conserve los productos agregados."""
    add_product_to_cart(menu_page, "7up", 2)

    cart_page.click(cart_page.BACK)
    assert cart_page.menu_is_visible()
    assert not cart_page.cart_is_visible()

    menu_page.open_cart()
    assert cart_page.get_quantity("7up", "Bebida", "En sitio") == 2
    assert cart_page.total() == "Total: $40"


def test_transfer_payment_shows_bank_details(menu_page, cart_page):
    """NO-018: Comprueba que transferencia muestre datos bancarios y efectivo los oculte."""
    add_product_to_cart(menu_page, "7up")

    cart_page.select_payment_method("Transferencia")

    details = cart_page.transfer_details()
    assert "Datos para Transferencia" in details
    assert "Banco:" in details
    assert "Beneficiario:" in details
    assert "CLABE:" in details
    assert cart_page.clickable(cart_page.CONTINUE).is_enabled()

    cart_page.select_payment_method("Efectivo")
    assert cart_page.payment_details_text() == ""
