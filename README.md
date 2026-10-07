# Pre-entrega Automation Testing – Joanna Lazarte

## Propósito del proyecto

Automatizar tres flujos básicos de navegación web sobre
[saucedemo.com](https://www.saucedemo.com/), un sitio diseñado para prácticas de testing:

1. **Login:** ingreso con credenciales válidas y validación de la redirección a `/inventory.html`.
2. **Catálogo:** verificación del título, de la presencia de productos y de los elementos
   importantes de la interfaz (menú, filtro, carrito), y lectura del nombre y precio del primer producto.
3. **Carrito:** agregar el primer producto, verificar el contador del carrito, navegar al carrito
   y comprobar que el producto agregado aparezca.

## Tecnologías utilizadas

- **Python 3.10+**
- **Pytest**: estructura y ejecución de los tests
- **pytest-html**: reporte HTML de resultados
- **Selenium WebDriver** (Chrome): automatización del navegador
- **Git y GitHub**: control de versiones

## Estructura del proyecto

```
├── tests/
│   ├── conftest.py          # Fixtures (driver, driver_logueado) y captura automática ante fallos
│   └── test_saucedemo.py    # Casos de prueba
├── utils/
│   ├── config.py            # URLs, credenciales y tiempos de espera
│   ├── driver_setup.py      # Creación y configuración del WebDriver
│   └── helpers.py           # Funciones auxiliares (login, esperas explícitas)
├── reports/
│   ├── reporte.html         # Reporte HTML de la última ejecución
│   └── evidencias/          # Ejemplos de captura de fallo y de logs de ejecución
├── pytest.ini               # Configuración de Pytest y markers
└── requirements.txt         # Dependencias
```

## Instalación de dependencias

Requisitos previos: tener **Python 3.10 o superior** y **Google Chrome** instalados.
Selenium descarga el driver de Chrome automáticamente, no hace falta instalarlo a mano.

```bash
git clone https://github.com/JoLazarte/pre-entrega-automation-testing-joanna-lazarte.git
cd pre-entrega-automation-testing-joanna-lazarte

python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo ejecutar las pruebas

Todos los tests, generando el reporte HTML:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

Otras opciones útiles:

```bash
pytest -v                       # Todos los tests, sin reporte
pytest -m smoke -v              # Solo los tests críticos (login y carrito)
pytest -m login -v              # Solo login
pytest -m catalogo -v           # Solo catálogo
pytest -m carrito -v            # Solo carrito
pytest -v -s                    # Muestra los print() en consola
HEADLESS=1 pytest -v            # Sin abrir ventana del navegador (en Windows: set HEADLESS=1)
```

## Casos de prueba

| Test | Marker | Qué valida |
|------|--------|-----------|
| `test_login_exitoso` | `smoke`, `login` | Redirección a `/inventory.html`, título "Swag Labs" y encabezado "Products" |
| `test_titulo_pagina_inventario` | `catalogo` | Título de la pestaña y encabezado de la sección |
| `test_productos_visibles` | `catalogo` | Existe al menos un producto y es visible |
| `test_elementos_interfaz_presentes` | `catalogo` | Menú, filtro de orden e ícono del carrito visibles |
| `test_nombre_y_precio_del_primer_producto` | `catalogo` | Nombre no vacío y precio con formato `$` |
| `test_agregar_producto_al_carrito` | `smoke`, `carrito` | Contador = 1, navegación al carrito y producto correcto dentro de él |

## Decisiones de diseño

- **Tests independientes:** cada test usa su propio navegador (fixture `driver`), por lo que la
  falla de uno no afecta a los demás. Los que necesitan sesión usan el fixture `driver_logueado`.
- **Esperas explícitas:** se usa `WebDriverWait` en los pasos críticos (formulario de login,
  badge del carrito, ítems del carrito) y no se mezclan con esperas implícitas.
- **Localizadores:** se prioriza ID → Name → CSS, y se evita XPath salvo que sea necesario.

## Evidencias

- **Reporte HTML:** `reports/reporte.html`.
- **Capturas automáticas ante fallos:** cuando un test falla se guarda un `.png` en
  `reports/screenshots/` y además queda incrustado en el reporte HTML. Esa carpeta está en
  `.gitignore`; en `reports/evidencias/` hay una captura de ejemplo.
- **Logs de ejecución:** cada corrida escribe `reports/ejecucion.log` (ignorado por Git).
  En `reports/evidencias/` hay un log de una ejecución exitosa y otro con un fallo.

## Nota sobre las credenciales

El usuario y la contraseña (`standard_user` / `secret_sauce`) son públicos: los publica el
propio sitio SauceDemo para practicar.