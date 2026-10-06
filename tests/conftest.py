"""Fixtures compartidos por todos los tests."""
import pytest

from utils.driver_setup import setup_driver


@pytest.fixture
def driver():
    """Abre un navegador nuevo para cada test y lo cierra al terminar.

    Al ser un driver por test, ninguno depende del estado de otro.
    """
    driver = setup_driver()
    yield driver
    driver.quit()