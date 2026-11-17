"""Composición de preprocesadores: `PreprocessingChain`.

Aplica una secuencia ordenada de `Preprocessor` y, al ser ella misma un
`Preprocessor`, el pipeline no distingue entre "un paso" y "una cadena de
pasos". Esto es lo que permite que el YAML declare varias cadenas distintas y
que el runner las trate de forma uniforme.

Incluye la cadena vacía (identidad), que sirve de BASELINE obligatorio: todo
experimento debe reportar también el resultado sin preprocesar, para poder
cuantificar cuánto aporta realmente cada preprocesado.
"""

from __future__ import annotations

from typing import Any, Sequence

from apple_seg.core.registry import PREPROCESSORS
from apple_seg.core.types import Image
from apple_seg.preprocessing.base import Preprocessor


@PREPROCESSORS.register("identity")
class Identity(Preprocessor):
    """Preprocesador nulo: devuelve la imagen tal cual. Baseline de referencia."""

    def apply(self, image: Image) -> Image:
        return image


class PreprocessingChain(Preprocessor):
    """Secuencia de preprocesadores aplicada en orden.

    Args:
        steps: Preprocesadores a aplicar, en orden.
        name: Identificador de la cadena (el campo `id` del YAML).
    """

    def __init__(self, steps: Sequence[Preprocessor] = (), name: str = "baseline") -> None:
        super().__init__()
        self.steps = list(steps)
        self.name = name

    def apply(self, image: Image) -> Image:
        raise NotImplementedError

    def get_params(self) -> dict[str, Any]:
        """Parámetros de todos los pasos, anidados por posición."""
        raise NotImplementedError

    @property
    def id(self) -> str:
        return self.name
