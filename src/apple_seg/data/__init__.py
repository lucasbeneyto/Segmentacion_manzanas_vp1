"""Bloque de datos: carga de imágenes y máscaras de referencia.

Clase padre del bloque: `ImageLoader`. Su responsabilidad es entregar objetos
`Sample` (imagen BGR uint8 + máscara bool) al pipeline, aislando al resto del
sistema de cómo esté organizado el dataset en disco.
"""

from apple_seg.data.dataset import AppleDataset
from apple_seg.data.loader import DiskImageLoader, ImageLoader

__all__ = ["ImageLoader", "DiskImageLoader", "AppleDataset"]
