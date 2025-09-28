#!/usr/bin/env python
"""Utilidad de línea de comandos de Django."""

import os
import sys

def main():
    """Punto de entrada para ejecutar tareas administrativas."""
    # Indica a Django qué archivo de configuración usar
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
    try:
        # Importa la función que ejecuta los comandos de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. "
            "¿Está instalado y activado el entorno virtual?"
        ) from exc
    # Ejecuta el comando recibido en consola (ej: runserver, makemigrations, etc.)
    execute_from_command_line(sys.argv)

# Si se ejecuta este archivo directamente, arranca la función main()
if __name__ == '__main__':
    main()
