from urllib.parse import urlsplit

from data import Links, OrderInfoCases, Products


def _assert_hosting_emulator(page):
    """Evita confirmar pedidos si la URL configurada no es el emulador local."""
    current_url = urlsplit(page.driver.current_url)
    configured_url = urlsplit(Links.URL_PUBLIC)
    local_hosts = {"127.0.0.1", "localhost"}
    assert (
        current_url.hostname in local_hosts
        and configured_url.hostname in local_hosts
        and current_url.port == 5000
        and configured_url.port == 5000
        and (current_url.scheme, current_url.netloc)
        == (configured_url.scheme, configured_url.netloc)
    ), (
        "Esta prueba confirma un pedido y solo debe ejecutarse contra Firebase "
        f"Hosting Emulator en {Links.URL_PUBLIC}."
    )


def _confirm_sample_order(menu_page, cart_page, payment_method):
    """Completa el flujo público hasta mostrar el resumen del pedido."""
    _assert_hosting_emulator(menu_page)
    menu_page.wait_until_menu_loaded()
    menu_page.choose_consume_type(OrderInfoCases.CONSUME_TYPE)
    menu_page.add_product(OrderInfoCases.PRODUCT_ID, OrderInfoCases.QUANTITY)
    menu_page.open_cart()
    cart_page.fill_client_name(OrderInfoCases.CUSTOMER)
    cart_page.select_payment_method(payment_method)
    cart_page.continue_order()


def test_public_checkout_shows_order_information(menu_page, cart_page, order_info_page):
    """NO-019–NO-020, NO-022–NO-023: valida el resumen y el ticket públicos."""
    _confirm_sample_order(menu_page, cart_page, OrderInfoCases.PAYMENT_METHOD)
    order_info_page.wait_until_visible(order_info_page.SCREEN)

    expected_total = Products.ITEMS[OrderInfoCases.PRODUCT_ID]["precio_base"]
    order_id = order_info_page.order_id()
    assert order_id
    assert order_info_page.customer() == OrderInfoCases.CUSTOMER
    assert order_info_page.payment_method() == OrderInfoCases.PAYMENT_METHOD
    assert order_info_page.total() == str(expected_total)
    assert Products.ITEMS[OrderInfoCases.PRODUCT_ID]["nombre"] in order_info_page.items_text()
    assert f"${expected_total}" in order_info_page.items_text()
    assert order_id in order_info_page.ticket_url()
    assert order_info_page.transfer_details() == ""

    order_info_page.click(order_info_page.BACK_TO_MENU)
    order_info_page.wait_until_visible(menu_page.SCREEN)
    assert not order_info_page.screen_is_visible()


def test_public_transfer_order_info_shows_bank_details_and_whatsapp(menu_page, cart_page, order_info_page):
    """NO-021: valida los datos bancarios y enlace de WhatsApp en el ticket público."""
    _confirm_sample_order(
        menu_page,
        cart_page,
        OrderInfoCases.TRANSFER_PAYMENT_METHOD,
    )
    order_info_page.wait_until_visible(order_info_page.SCREEN)

    assert order_info_page.payment_method() == OrderInfoCases.TRANSFER_PAYMENT_METHOD
    transfer_details = order_info_page.transfer_details()
    assert "Datos para Transferencia" in transfer_details
    assert "Banco:" in transfer_details
    assert "Beneficiario:" in transfer_details
    assert "CLABE:" in transfer_details
    assert order_info_page.whatsapp_url().startswith("https://wa.me/")
