
# 📷 Escáner de Códigos de Barras Profesional (HUD Edition)

> Sistema de escaneo en tiempo real con interfaz Head-Up Display (HUD), identificación de productos, registro automático en Excel y feedback auditivo. Diseñado para entornos de alta eficiencia y estética industrial.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Status](https://img.shields.io/badge/status-production-green.svg)

## ✨ Características Principales

*   **⚡ Escaneo en Tiempo Real**: Captura y decodificación asíncrona de video para máxima fluidez.
*   **🖥️ Interfaz HUD Premium**: Diseño estilo "Dark Industrial" con paneles semitransparentes, indicadores de rastreo y estética técnica.
*   **🔍 Identificación de Productos**: Base de datos integrada para reconocer productos específicos (ej. "Libreta Azul", "Crema de Manos") al instante.
*   **📊 Registro Automático**: Exportación automática de cada escaneo a un archivo Excel (`scans.xlsx`) con timestamp.
*   **🔊 Feedback Auditivo**: Confirmación sonora (PIP) tras cada lectura exitosa para operaciones "eyes-free".
*   **🛡️ Robustez y Fiabilidad**: Algoritmo de "Debouncing" (1s) para evitar lecturas falsas o duplicadas por error.
*   **📦 Gestión de Inventario**: Contadores automáticos con lógica de "Cooldown" (2s) para re-escanear productos intencionalmente.

## 🛠️ Stack Tecnológico

*   **Core**: Python 3.12+ (Gestionado con `uv`)
*   **Visión por Computador**: OpenCV (`cv2`) para captura y dibujo UI.
*   **Decodificación**: PyZbar (`zbar`) para lectura de códigos 1D/2D.
*   **Datos**: OpenPyXL para integración con Excel.
*   **Audio**: Requerimientos nativos del SO (`winsound`).
*   **Arquitectura**: `asyncio` para concurrencia no bloqueante.

## 🚀 Guía de Instalación

Sigue estos pasos para configurar el entorno de desarrollo desde cero.

### Prerrequisitos
*   Python 3.12 o superior.
*   `uv` (Gestor de paquetes de Python moderno).
*   Cámara web funcional.

### Pasos

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tu-usuario/camara-lectro.git
    cd camara-lectro
    ```

2.  **Instalar dependencias con `uv`**:
    El proyecto utiliza `pyproject.toml` para gestionar dependencias de forma determinista.
    ```bash
    uv sync
    ```
    *Esto creará un entorno virtual `.venv` e instalará todas las librerías necesarias.*

3.  **Verificar instalación**:
    ```bash
    uv run python --version
    # Debería mostrar Python 3.12.x
    ```

## 🎮 Uso

Para iniciar el escáner:

```bash
uv run python src/main.py
```

### Controles
*   **`q`**: Salir de la aplicación.
*   **Escaneo**: Simplemente apunta la cámara a un código de barras.

### Flujo de Trabajo
1.  El sistema muestra el video en una ventana "Dark Mode".
2.  Al detectar un código, dibuja un recuadro verde (o rojo si no reconocido).
3.  Si el código se mantiene estable por 1 segundo, se confirma la lectura.
4.  Suena un "PIP", se registra en Excel y se actualiza el HUD lateral.
5.  Para volver a escanear el mismo producto, retíralo de la vista por 2 segundos.

## 🏗️ Arquitectura y Decisiones (ADR)

*   **ADR-001: Asyncio**: Se decidió usar `asyncio` para desacoplar la captura de video del procesamiento de frames, evitando que la UI se congele durante operaciones de disco (Excel).
*   **ADR-002: Debouncing**: Se implementó un buffer de validación temporal para filtrar "ruido" y lecturas parciales, garantizando solo datos de alta confianza.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de enviar un PR.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
