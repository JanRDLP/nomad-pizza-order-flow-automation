# Nomad Pizza: automatización del flujo público de pedidos

Proyecto de pruebas de interfaz para el recorrido público de compra de Nomad Pizza. Usa **Python, pytest y Selenium** con Page Objects y datos parametrizados para validar menú y carrito.

Este paquete contiene únicamente pruebas y Page Objects de la experiencia pública. No incluye el código de la aplicación, la interfaz administrativa, pruebas de administración, credenciales, `.env` ni integraciones de limpieza para Firestore.

## Alcance

- **Menú:** visibilidad y nombre de productos, contadores, tipo de consumo, precios y promoción de Pizza Dog.
- **Pizzas personalizables:** disponibilidad de ingredientes entre selectores, combinaciones y precio según los ingredientes elegidos.
- **Carrito:** cantidades, subtotales y total del pedido; confirmación al disminuir de uno a cero; consistencia de datos del producto; acciones de eliminar y volver; datos bancarios al elegir transferencia.
- **Información del pedido público:** resumen, identificador, cliente, método de pago, total, productos, enlace del ticket/QR, botón para volver al menú y datos de transferencia/WhatsApp.

Las pruebas de menú y carrito se detienen antes de confirmar. Las dos pruebas de información sí completan una compra de prueba para llegar al resumen y por eso están protegidas para ejecutarse únicamente en Firebase Hosting Emulator local (puerto 5000). Los pedidos permanecen en Firestore Emulator; no se borran automáticamente. No se incluye la prueba del aviso de pedido nuevo, que pertenece a la experiencia administrativa.

## Requisitos

- Python 3.10 o posterior.
- Google Chrome.
- Una URL accesible de la aplicación pública. Por defecto se usa Firebase Hosting Emulator en `http://127.0.0.1:5000/`.
- Para `test_info.py`, Firebase Auth y Firestore Emulator deben estar disponibles además de Hosting Emulator.

## Instalación y ejecución

Desde la carpeta de este proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si ejecutarás las pruebas contra otra URL pública, configura la variable para la terminal actual:

```powershell
$env:NOMAD_PUBLIC_URL = "https://tu-sitio-publico.example/"
```

Ejecuta el flujo público:

```powershell
python -m pytest tests/test_menu.py tests/test_cart.py -v
```

Las pruebas de información confirman pedidos locales. Ejecútalas solo con Firebase Emulators en marcha:

```powershell
python -m pytest tests/test_info.py -v
```

Las combinaciones de ingredientes son parametrizadas y pueden generar numerosos casos en la ejecución.

## Estructura

```text
public-order-flow/
├── conftest.py
├── data.py
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

## Publicarlo en GitHub

Inicializa Git **dentro de esta carpeta `public-order-flow`**, para que el repositorio contenga solo este paquete y no la suite administrativa ni los archivos privados del proyecto completo. Antes de publicar, revisa los archivos que se agregarán:

```powershell
git init
git add .
git status --short
```

Confirma que el listado solo incluya los archivos descritos en la estructura anterior. Después crea el commit y agrega el remoto de tu nuevo repositorio:

```powershell
git commit -m "Public order flow automation"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

No inicialices Git en la carpeta padre `test-nomad-pizza` para este repositorio público: ahí permanece la suite completa, incluidas las pruebas y Page Objects de administración.
