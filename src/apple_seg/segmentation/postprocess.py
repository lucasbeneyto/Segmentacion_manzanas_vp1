"""Refinado de máscaras: clase padre `MaskRefiner` y composición `RefinementChain`.

Pertenece al bloque de segmentación porque opera sobre máscaras binarias, no
sobre imágenes. Se declara como componente aparte (y opcional) del segmentador
para poder medir en las tablas finales cuánto mejora cada método al refinarse,
en lugar de esconder la morfología dentro de cada `segment`.

Contrato: máscara bool (H, W) -> máscara bool (H, W), misma forma.

Las implementaciones concretas (morfología, relleno de huecos, filtrado por
área o por forma, separación de objetos en contacto, ...) las añade el equipo
en módulos propios. Plantilla a copiar:
`segmentation/EJEMPLO_segmentador.py` -> clase `EjemploRefinador`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from apple_seg.core.types import Mask


class MaskRefiner(ABC):
    """CLASE PADRE del refinado de máscaras.

    Subclases: implementar únicamente `apply`.
    """

    def __init__(self, **params: Any) -> None:
        self.params: dict[str, Any] = params

    @abstractmethod
    def apply(self, mask: Mask) -> Mask:
        """Devuelve la máscara refinada, bool y con la misma forma que la entrada."""

    def __call__(self, mask: Mask) -> Mask:
        return self.apply(mask)

    def get_params(self) -> dict[str, Any]:
        """Parámetros del refinador (se vuelcan en el informe del experimento)."""
        return dict(self.params)

    @property
    def id(self) -> str:
        """Identificador legible usado en tablas y nombres de ficheros."""
        return type(self).__name__

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.get_params()}>"


class RefinementChain(MaskRefiner):
    """Secuencia ordenada de refinadores; es a su vez un `MaskRefiner`.

    Permite declarar en el YAML varios pasos de refinado y que el segmentador
    los trate como uno solo.
    """

    def __init__(self, steps: Sequence[MaskRefiner] = (), name: str = "refine") -> None:
        super().__init__()
        self.steps = list(steps)
        self.name = name

    def apply(self, mask: Mask) -> Mask:
        raise NotImplementedError

    def get_params(self) -> dict[str, Any]:
        """Parámetros de todos los pasos, anidados por posición."""
        raise NotImplementedError

    @property
    def id(self) -> str:
        return self.name
