"""Contrato del bloque de segmentación: la clase padre `Segmenter`.

REGLA DEL CONTRATO
    entrada : imagen BGR uint8 (H, W, 3) -- la que devuelve el preprocesador
    salida  : máscara bool (H, W), True = píxel de manzana

Puntos clave para quien implemente un segmentador nuevo:
    - `segment` NO debe modificar la imagen de entrada.
    - La máscara devuelta debe tener el mismo (H, W) que la imagen recibida.
    - Si el método necesita estimar parámetros a partir de datos (umbrales
      aprendidos de histogramas, centroides de color, ...), se hace en `fit`,
      que el runner llama solo con el split de desarrollo. Los métodos sin
      ajuste heredan la implementación vacía por defecto.
    - El refinado morfológico se declara aparte (`refiner`) para poder medir
      cuánto aporta, en lugar de esconderlo dentro de cada método.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable

from apple_seg.core.types import Image, Mask, Sample


class Segmenter(ABC):
    """CLASE PADRE del bloque de segmentación.

    Subclases: implementar `segment`; opcionalmente sobrescribir `fit`.

    Attributes:
        registry_name: Nombre de registro (lo asigna @SEGMENTERS.register).
        refiner: Refinador de máscara opcional aplicado tras `segment`.
    """

    registry_name: str = "segmenter"
    requires_fit: bool = False

    def __init__(self, refiner: Any | None = None, **params: Any) -> None:
        self.params: dict[str, Any] = params
        self.refiner = refiner
        self.is_fitted: bool = False

    @abstractmethod
    def segment(self, image: Image) -> Mask:
        """Devuelve la máscara binaria de manzanas para la imagen dada."""

    def fit(self, samples: Iterable[Sample]) -> "Segmenter":
        """Ajusta parámetros sobre el split de desarrollo. Por defecto, no-op."""
        self.is_fitted = True
        return self

    def predict(self, image: Image) -> Mask:
        """`segment` + refinado opcional. Es lo que invoca el pipeline."""
        mask = self.segment(image)
        if self.refiner is not None:
            mask = self.refiner(mask)
        return mask

    def __call__(self, image: Image) -> Mask:
        return self.predict(image)

    def get_params(self) -> dict[str, Any]:
        """Parámetros del método (se vuelcan en el informe del experimento)."""
        return dict(self.params)

    @property
    def id(self) -> str:
        """Identificador legible usado en tablas y nombres de ficheros."""
        return getattr(self, "name", None) or self.registry_name

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.id}>"
