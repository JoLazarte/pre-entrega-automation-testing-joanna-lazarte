"""Fixtures compartidos por todos los tests."""
import pytest
from selenium.webdriver.common.by import By

from utils.driver_setup import setup_driver
from utils.helpers import esperar_visible, login


@pytest.fixture
def driver():
    """Abre un navegador nuevo para cada test y lo cierra al terminar.

    Al ser un driver por test, ninguno depende del estado de otro.
    """
    driver = setup_driver()
    yield driver
    driver.quit()


@pytest.fixture
def driver_logueado(driver):
    """Devuelve un driver con la sesión iniciada y el inventario ya cargado."""
    login(driver)
    # Espera explícita: el catálogo debe estar visible antes de empezar el test
    esperar_visible(driver, (By.CLASS_NAME, "inventory_item"))
    return driver