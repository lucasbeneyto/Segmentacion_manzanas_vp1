"""Cargador de imágenes: contrato `ImageLoader` + implementación sobre disco.

Responsabilidades del bloque:
    - localizar los pares (imagen, máscara de referencia),
    - leerlos con OpenCV,
    - normalizarlos a las convenciones de `core.types` (BGR uint8 / bool),
    - entregar objetos `Sample`.

Ningún otro módulo debe leer ficheros del dataset directamente.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

from apple_seg.core.types import Mask, Sample


class ImageLoader(ABC):
    """CLASE PADRE del bloque de datos.

    Un loader es iterable y direccionable por índice; expone además los
    identificadores de las muestras para poder hacer splits reproducibles.
    """

    @abstractmethod
    def __len__(self) -> int:
        """Número de muestras disponibles."""

    @abstractmethod
    def __getitem__(self, index: int) -> Sample:
        """Devuelve la muestra i-ésima ya normalizada."""

    @abstractmethod
    def sample_ids(self) -> list[str]:
        """Lista de identificadores, en el mismo orden que la indexación."""

    def __iter__(self) -> Iterator[Sample]:
        for i in range(len(self)):
            yield self[i]


class DiskImageLoader(ImageLoader):
    """Loader para un dataset en disco con carpetas paralelas de imágenes y máscaras.

    Empareja cada imagen con su máscara aplicando `mask_template` sobre el nombre
    base del fichero (p. ej. "{stem}.png" o "{stem}_mask.png"), de forma que
    soporta las convenciones de nombrado habituales sin cambiar código.

    Args:
        images_dir: Carpeta de imágenes originales.
        masks_dir: Carpeta de máscaras de referencia (None = inferencia sin GT).
        image_glob: Patrón de búsqueda de imágenes.
        mask_template: Plantilla del nombre de la máscara a partir del stem.
        resize: (ancho, alto) opcional; si se usa, la máscara se reescala con
            interpolación NEAREST para no inventar píxeles.
        limit: Carga solo las N primeras muestras (útil para pruebas rápidas).
    """

    def __init__(
        self,
        images_dir: str | Path,
        masks_dir: str | Path | None = None,
        image_glob: str = "*",
        mask_template: str = "{stem}.png",
        resize: tuple[int, int] | None = None,
        limit: int | None = None,
    ) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __getitem__(self, index: int) -> Sample:
        raise NotImplementedError

    def sample_ids(self) -> list[str]:
        raise NotImplementedError

    def _read_mask(self, path: Path) -> Mask:
        """Lee y binariza una máscara de referencia a bool (True = manzana)."""
        raise NotImplementedError
