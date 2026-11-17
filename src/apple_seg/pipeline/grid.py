"""Construcción del espacio de experimentos: `CombinationGrid`.

Genera las combinaciones (preprocesador x segmentador) que se van a ejecutar y
les asigna un identificador estable, usado en nombres de carpeta, leyendas de
figuras y filas de las tablas.

Permite además excluir combinaciones sin sentido (p. ej. un segmentador que ya
trabaja en Lab combinado con un preprocesador que fuerza HSV) mediante la clave
`exclude` de la configuración, para no malgastar tiempo de cómputo.
"""

from __future__ import annotations

from typing import Iterator, Sequence

from apple_seg.preprocessing.base import Preprocessor
from apple_seg.segmentation.base import Segmenter


class CombinationGrid:
    """Producto cartesiano de preprocesadores y segmentadores."""

    def __init__(
        self,
        preprocessors: Sequence[Preprocessor],
        segmenters: Sequence[Segmenter],
        exclude: Sequence[tuple[str, str]] = (),
    ) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[tuple[Preprocessor, Segmenter]]:
        raise NotImplementedError

    def combo_ids(self) -> list[str]:
        """Identificadores '<preproc_id>+<segmenter_id>' de todas las combinaciones."""
        raise NotImplementedError
