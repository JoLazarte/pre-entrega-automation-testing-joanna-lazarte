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

@pytest.mark.catalogo
def test_titulo_pagina_inventario(driver_logueado):
    """El título de la pestaña y el encabezado de la sección deben ser correctos."""
    driver = driver_logueado

    assert driver.title == "Swag Labs", f"Título de pestaña incorrecto: '{driver.title}'"

    encabezado = esperar_visible(
        driver, (By.CSS_SELECTOR, "div.header_secondary_container .title")
    )
    assert encabezado.text == "Products", f"Encabezado incorrecto: '{encabezado.text}'"


@pytest.mark.catalogo
def test_productos_visibles(driver_logueado):
    """Debe haber al menos un producto visible en el catálogo."""
    driver = driver_logueado

    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) >= 1, "No se encontró ningún producto en el catálogo"
    assert productos[0].is_displayed(), "El primer producto no está visible"
    print(f"Se encontraron {len(productos)} productos")


@pytest.mark.catalogo
def test_elementos_interfaz_presentes(driver_logueado):
    """El menú, el filtro de orden y el carrito deben estar presentes y visibles."""
    driver = driver_logueado

    elementos_clave = {
        "menú hamburguesa": (By.ID, "react-burger-menu-btn"),
        "filtro de orden": (By.CLASS_NAME, "product_sort_container"),
        "ícono del carrito": (By.CLASS_NAME, "shopping_cart_link"),
    }

    for nombre, localizador in elementos_clave.items():
        elemento = driver.find_element(*localizador)
        assert elemento.is_displayed(), f"El elemento '{nombre}' no está visible"


@pytest.mark.catalogo
def test_nombre_y_precio_del_primer_producto(driver_logueado):
    """Lista el nombre y el precio del primer producto y valida que existan."""
    driver = driver_logueado

    primer_producto = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
    # Se busca DENTRO de la tarjeta del primer producto, no en toda la página
    nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text

    assert nombre != "", "El nombre del primer producto está vacío"
    assert precio.startswith("$"), f"El precio no tiene el formato esperado: '{precio}'"
    print(f"Primer producto: {nombre} - {precio}")