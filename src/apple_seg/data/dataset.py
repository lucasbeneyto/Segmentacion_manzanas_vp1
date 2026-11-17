"""Vista de alto nivel del dataset: estadísticas, filtrado y subconjuntos.

`AppleDataset` envuelve a un `ImageLoader` y añade lo que el pipeline y la
memoria del proyecto necesitan saber del conjunto de datos: número de imágenes,
resolución, porcentaje medio de píxeles de manzana, muestras con/sin fruto, etc.
También permite quedarse con un subconjunto (split o selección manual) sin
duplicar imágenes en memoria.
"""

from __future__ import annotations

from typing import Iterator, Sequence

from apple_seg.data.loader import ImageLoader
from apple_seg.core.types import Sample


class AppleDataset:
    """Conjunto de muestras con utilidades de inspección y submuestreo."""

    def __init__(self, loader: ImageLoader, indices: Sequence[int] | None = None) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Sample]:
        raise NotImplementedError

    def subset(self, indices: Sequence[int]) -> "AppleDataset":
        """Nueva vista del dataset limitada a los índices dados."""
        raise NotImplementedError

    def describe(self) -> dict:
        """Estadísticas descriptivas del conjunto (para la memoria del proyecto)."""
        raise NotImplementedError
