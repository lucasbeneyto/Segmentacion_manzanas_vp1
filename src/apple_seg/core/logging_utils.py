"""Configuración del logging del proyecto.

Un único `get_logger(__name__)` para todos los módulos, con formato homogéneo y
nivel controlable desde la CLI (-v / --quiet). Evita `print` disperso por el
código, que ensucia la salida del pipeline cuando se ejecutan muchas
combinaciones.
"""

from __future__ import annotations

import logging


def setup_logging(level: int = logging.INFO) -> None:
    """Configura el logger raíz del proyecto (formato, nivel, handler de consola)."""
    raise NotImplementedError


def get_logger(name: str) -> logging.Logger:
    """Devuelve el logger del módulo indicado."""
    return logging.getLogger(name)
