"""Infraestructura transversal: tipos de datos, registro de componentes y configuración.

Este subpaquete no contiene lógica de visión por computador: solo las piezas
comunes de las que dependen los tres bloques principales.
"""

from apple_seg.core.registry import METRICS, PREPROCESSORS, SEGMENTERS, Registry
from apple_seg.core.types import Image, Mask, Prediction, Sample

__all__ = [
    "Image",
    "Mask",
    "Sample",
    "Prediction",
    "Registry",
    "PREPROCESSORS",
    "SEGMENTERS",
    "METRICS",
]
