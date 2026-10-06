import os
from itertools import combinations


class Links:
    """URL de la aplicación pública que recorrerán las pruebas."""

    URL_PUBLIC = os.getenv("NOMAD_PUBLIC_URL", "http://127.0.0.1:5000/")


class Dropdown:
    """Opciones públicas de consumo, pago e ingredientes."""

    CONSUME = ["En sitio", "Para llevar"]
    PAYMENT = ["Efectivo", "Tarjeta", "Transferencia"]
    INGREDIENTS = [
        "Aceituna",
        "Champiñón",
        "Jamón",
        "Peperoni",
        "Salami",
        "Tocino",
        "Salchicha",
    ]


class IngredientCases:
    """Combinaciones de ingredientes para la pizza personalizable."""

    MAX_INGREDIENTS = 3
    ALL_COMBINATIONS = [
        combination
        for quantity in range(1, min(MAX_INGREDIENTS, len(Dropdown.INGREDIENTS)) + 1)
        for combination in combinations(Dropdown.INGREDIENTS, quantity)
    ]


class Products:
    """Datos visibles del catálogo público usados como valores esperados."""

    EXTRA_INGREDIENT_PRICE = 16
    ITEMS = {
        "pizza_dog": {
            "nombre": "Pizza Dog",
            "precio_base": 60,
            "descripcion": (
                "Masa fermentada con salchicha de res ahumada cubierta de salsa de tomate "
                "de la casa y mezcla de quesos."
            ),
            "tipo": "pizza",
            "temporal": False,
            "promo": "2x100_para_llevar",
            "ingredientes_extra": None,
        },
        "pizza_nomad": {
            "nombre": "Pizza Nomad",
            "precio_base": 80,
            "descripcion": (
                "Masa fermentada acompañada de salsa de la casa con mezcla de queso "
                "mozzarella y parmesano con hierbas italianas."
            ),
            "tipo": "pizza_personalizable",
            "temporal": False,
            "promo": None,
            "ingredientes_extra": EXTRA_INGREDIENT_PRICE,
        },
        "agua_jamaica": {
            "nombre": "Agua de Jamaica",
            "precio_base": 20,
            "descripcion": "Agua fresca",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
        "7up": {
            "nombre": "7up",
            "precio_base": 20,
            "descripcion": "Refresco",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
        "agua_natural": {
            "nombre": "Agua Natural",
            "precio_base": 20,
            "descripcion": "Agua",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
        "manzana": {
            "nombre": "Manzana",
            "precio_base": 20,
            "descripcion": "Refresco",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
        "pepsi": {
            "nombre": "Pepsi",
            "precio_base": 20,
            "descripcion": "Refresco",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
        "squirt": {
            "nombre": "Squirt",
            "precio_base": 20,
            "descripcion": "Refresco",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
        "te": {
            "nombre": "Té",
            "precio_base": 20,
            "descripcion": "Agua fresca",
            "tipo": "bebida",
            "temporal": False,
            "promo": None,
        },
    }


    class OrderInfoCases:
        """Datos del pedido mínimo que se confirma para validar su información."""

        CUSTOMER = "QA Flujo Público"
        PRODUCT_ID = "7up"
        QUANTITY = 1
        CONSUME_TYPE = "En sitio"
        PAYMENT_METHOD = "Efectivo"
        TRANSFER_PAYMENT_METHOD = "Transferencia"


    @classmethod
    def personalizable_ids(cls):
        """Devuelve los productos que permiten elegir ingredientes adicionales."""
        return [
            product_id
            for product_id, product in cls.ITEMS.items()
            if product.get("tipo") == "pizza_personalizable"
        ]



