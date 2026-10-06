"""Tests de automatización sobre saucedemo.com."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import EXPLICIT_WAIT_SECONDS, INVENTORY_URL_FRAGMENT
from utils.helpers import esperar_visible, login


@pytest.mark.smoke
@pytest.mark.login
def test_login_exitoso(driver):
    """Un usuario válido debe ser redirigido a la página de inventario."""
    login(driver)

    # Espera explícita a que la URL cambie al inventario
    WebDriverWait(driver, EXPLICIT_WAIT_SECONDS).until(
        EC.url_contains(INVENTORY_URL_FRAGMENT)
    )
    assert INVENTORY_URL_FRAGMENT in driver.current_url, (
        f"Se esperaba estar en {INVENTORY_URL_FRAGMENT}, pero la URL es {driver.current_url}"
    )

    # Validación del título de la pestaña
    assert driver.title == "Swag Labs", (
        f"Título de pestaña incorrecto: '{driver.title}'"
    )

    # Validación del encabezado de la sección
    encabezado = esperar_visible(
        driver, (By.CSS_SELECTOR, "div.header_secondary_container .title")
    )
    assert encabezado.text == "Products", (
        f"Encabezado incorrecto: '{encabezado.text}'"
    )

    print("Test OK")