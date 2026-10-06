"""Fixtures y hooks compartidos por todos los tests."""
import logging
from datetime import datetime

import pytest
from pytest_html import extras
from selenium.webdriver.common.by import By

from utils.config import SCREENSHOTS_DIR
from utils.driver_setup import setup_driver
from utils.helpers import esperar_visible, login

logger = logging.getLogger(__name__)


@pytest.fixture
def driver(request):
    """Abre un navegador nuevo para cada test y lo cierra al terminar.

    Al ser un driver por test, ninguno depende del estado de otro.
    """
    logger.info("Abriendo navegador para: %s", request.node.name)
    driver = setup_driver()
    yield driver
    logger.info("Cerrando navegador de: %s", request.node.name)
    driver.quit()


@pytest.fixture
def driver_logueado(driver):
    """Devuelve un driver con la sesión iniciada y el inventario ya cargado."""
    login(driver)
    # Espera explícita: el catálogo debe estar visible antes de empezar el test
    esperar_visible(driver, (By.CLASS_NAME, "inventory_item"))
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Registra el resultado de cada test y, si falla, guarda una captura.

    La captura se guarda como archivo .png y también se incrusta en el reporte HTML.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    logger.info("Resultado de %s: %s", item.name, report.outcome.upper())

    if report.failed:
        # El driver llega al test con alguno de estos dos nombres de fixture
        driver = item.funcargs.get("driver") or item.funcargs.get("driver_logueado")
        if driver is None:
            return

        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        marca_de_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = SCREENSHOTS_DIR / f"{item.name}_{marca_de_tiempo}.png"
        driver.save_screenshot(str(ruta))
        logger.error("Test fallido: %s. Captura guardada en %s", item.name, ruta)

        # Se incrusta en el reporte HTML en base64 (funciona con --self-contained-html)
        report.extras = getattr(report, "extras", []) + [
            extras.image(driver.get_screenshot_as_base64())
        ]