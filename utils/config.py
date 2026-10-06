"""Configuración central del proyecto: URLs, credenciales y tiempos de espera."""

BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL_FRAGMENT = "/inventory.html"

# Credenciales válidas de SauceDemo (sitio de práctica, son públicas)
VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

# Tiempo máximo (en segundos) para las esperas explícitas
EXPLICIT_WAIT_SECONDS = 10