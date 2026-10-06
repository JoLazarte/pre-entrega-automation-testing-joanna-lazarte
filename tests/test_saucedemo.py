"""Tests de automatización sobre saucedemo.com."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import CART_URL_FRAGMENT, EXPLICIT_WAIT_SECONDS, INVENTORY_URL_FRAGMENT
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

@pytest.mark.smoke
@pytest.mark.carrito
def test_agregar_producto_al_carrito(driver_logueado):
    """Agrega el primer producto, verifica el contador y lo busca dentro del carrito."""
    driver = driver_logueado

    # 1) Ubicar el primer producto y guardar su nombre para compararlo después
    primer_producto = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
    nombre_esperado = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text

    # 2) Agregarlo al carrito (el botón está dentro de la tarjeta del producto)
    primer_producto.find_element(By.TAG_NAME, "button").click()

    # 3) Espera explícita al badge del carrito y verificación del contador
    badge = esperar_visible(driver, (By.CLASS_NAME, "shopping_cart_badge"))
    assert badge.text == "1", f"El contador del carrito debería mostrar 1, pero muestra '{badge.text}'"

    # 4) Navegar al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, EXPLICIT_WAIT_SECONDS).until(EC.url_contains(CART_URL_FRAGMENT))
    assert CART_URL_FRAGMENT in driver.current_url, (
        f"No se llegó al carrito, la URL es {driver.current_url}"
    )

    # 5) Verificar que el producto agregado aparece en el carrito
    # Espera explícita: los ítems se renderizan después del cambio de URL
    esperar_visible(driver, (By.CLASS_NAME, "cart_item"))
    items_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items_carrito) == 1, f"Se esperaba 1 ítem en el carrito, hay {len(items_carrito)}"

    nombre_en_carrito = items_carrito[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    assert nombre_en_carrito == nombre_esperado, (
        f"En el carrito aparece '{nombre_en_carrito}', se esperaba '{nombre_esperado}'"
    )

    print("Test OK")