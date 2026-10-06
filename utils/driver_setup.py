"""Funciones para crear y configurar el WebDriver de Chrome."""
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_driver():
    """Crea y devuelve una instancia de Chrome lista para usar.

    Si la variable de entorno HEADLESS=1 está definida, corre sin ventana.
    """
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Evita los pop-ups de Chrome sobre guardar/filtrar contraseñas,
    # que pueden tapar elementos y romper los clics
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver