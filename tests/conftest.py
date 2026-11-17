"""Fixtures compartidas por las pruebas.

Proporciona imágenes y máscaras sintéticas (discos rojos sobre fondo verde) que
permiten comprobar el contrato de cada bloque sin depender del dataset real,
que no se versiona en el repositorio.
"""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def synthetic_sample():
    """Imagen sintética con dos 'manzanas' circulares y su máscara exacta."""
    raise NotImplementedError
