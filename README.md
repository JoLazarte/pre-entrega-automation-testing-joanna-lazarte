# Pre-entrega Automation Testing – Joanna Lazarte

## Propósito
Automatizar con Selenium y Pytest tres flujos básicos de
[saucedemo.com](https://www.saucedemo.com/): login, navegación del catálogo
y carrito de compras.

## Tecnologías
- Python
- Pytest + pytest-html
- Selenium WebDriver (Chrome)
- Git y GitHub

## Instalación
```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución
```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

## Estructura
- `tests/`: casos de prueba
- `utils/`: funciones auxiliares
- `reports/`: reportes HTML y capturas de pantalla