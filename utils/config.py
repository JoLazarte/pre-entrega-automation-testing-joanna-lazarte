"""Configuración central del proyecto: URLs, credenciales y tiempos de espera."""

from pathlib import Path

# Carpeta donde se guardan las capturas de los tests fallidos
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = RAIZ_PROYECTO / "reports" / "screenshots"

BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL_FRAGMENT = "/inventory.html"
CART_URL_FRAGMENT = "/cart.html"

# Credenciales válidas de SauceDemo (sitio de práctica, son públicas)
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

# Tiempo máximo (en segundos) para las esperas explícitas
EXPLICIT_WAIT_SECONDS = 10