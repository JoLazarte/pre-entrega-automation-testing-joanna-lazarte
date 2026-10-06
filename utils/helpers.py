"""Funciones auxiliares reutilizables por los tests."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import BASE_URL, EXPLICIT_WAIT_SECONDS, VALID_PASSWORD, VALID_USER


def esperar_visible(driver, locator, timeout=EXPLICIT_WAIT_SECONDS):
    """Espera explícitamente a que un elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def login(driver, usuario=VALID_USER, password=VALID_PASSWORD):
    """Abre SauceDemo e inicia sesión con las credenciales indicadas."""
    driver.get(BASE_URL)

    # Espera explícita: el formulario debe estar visible antes de escribir
    campo_usuario = esperar_visible(driver, (By.ID, "user-name"))
    campo_usuario.send_keys(usuario)

    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()