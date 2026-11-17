"""Contrato del bloque de preprocesado: la clase padre `Preprocessor`.

REGLA DEL CONTRATO
    entrada : imagen BGR uint8 (H, W, 3)
    salida  : imagen BGR uint8 (H, W, 3) con el MISMO alto y ancho

Mantener forma y tipo es lo que hace que cualquier preprocesador se pueda
encadenar con cualquier otro y conectar con cualquier segmentador. Un paso que
necesite trabajar en otro espacio de color (HSV, Lab, gris) debe convertir de
vuelta a BGR antes de devolver el resultado. Si un paso necesita redimensionar o
recortar, debe dejar el tamaño original en los metadatos de la muestra para que el
runner revierta la máscara antes de evaluarla.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apple_seg.core.types import Image


class Preprocessor(ABC):
    """CLASE PADRE del bloque de preprocesado.

    Subclases: implementar únicamente `apply`. El resto (identificación,
    parámetros, trazabilidad) lo resuelve la clase base.

    Attributes:
        registry_name: Nombre con el que la clase está registrada (lo asigna el
            decorador @PREPROCESSORS.register).
    """

    registry_name: str = "preprocessor"

    def __init__(self, **params: Any) -> None:
        self.params: dict[str, Any] = params

    @abstractmethod
    def apply(self, image: Image) -> Image:
        """Transforma la imagen. DEBE devolver BGR uint8 con el mismo (H, W)."""

    def __call__(self, image: Image) -> Image:
        """Azúcar sintáctico: `preproc(img)` equivale a `preproc.apply(img)`."""
        return self.apply(image)

    def get_params(self) -> dict[str, Any]:
        """Parámetros del componente (se vuelcan en el informe del experimento)."""
        return dict(self.params)

    @property
    def id(self) -> str:
        """Identificador legible usado en tablas y nombres de ficheros."""
        if not self.params:
            return self.registry_name
        args = ",".join(f"{k}={v}" for k, v in sorted(self.params.items()))
        return f"{self.registry_name}({args})"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.id}>"
